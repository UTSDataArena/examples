
## Distributed rendering with omegalib+osg+equalizer

When programming an application in omegalib, the underlying displaysystem (equalizer) is mostly opaque to the programmer. It is however important to understand what is going on, when programming for a distributed, parallel rendering environment such as the Data Arena. 

##### What is parallel rendering ?
Quoting the introduction chapter of the Equalizer programming guide:

(insert figure 1 of equalizer programming guide)

Figure ? illustrates the basic principle of any parallel rendering application. The  typical OpenGL application, for example using GLUT, has an event loop which redraws the scene, updates application data based on received events, and eventually renders a new frame.
A parallel rendering application uses the same basic execution model, extending it by separating the rendering code from the main event loop. The rendering code is then executed in parallel on different resources, depending on the configuration chosen at runtime.

##### How does parallel rendering work in omegalib ?

(insert diagramOmegaFrame.png)

Rendering a frame with omegalib 

The EqualizerDisplaySystem in omegalib runs the mainloop and calls the Configimpl startFrame method. ConfigImpl is a implementation of the Config class methods in Equalizer. For an in-depth discussion of the various Equalizer concepts, check out the Equalizer Programming Guide, it is recommended to read the Introduction chapter and the "Equalizer Parallel Rendering Framework" chapter. 


The master, which drives the slaves rendering, first shares all Events to all nodes, each node is then reponsible for handling these Events. When handling events, commonly things such as calculating the new camera position are performed. Then other shared data is synced, for example a user could sync the position of an object across the nodes. Next the update call is performed on the master, which calls the update method on all registered modules. The update method internally calculates the correct offset of each screen camera, therefore the camera position should not be changed after the update traversal anymore. The update callback is also the place for the user to do any larger computations, such as running a physics simulation step. The startFrame(version) method tells all slave nodes to update themselves. It carries the frame version to sync all nodes to render the same frame. After all updates have been performed all nodes render the frame, which translates to calls to the osgModule, which executes culling and drawing traversals. Finally all nodes are synced on the end of the frame again.

Of course, this process has some intrecate issues that can arise when building complex applications. Often looking at the source code of omegalib, without having to extensively debug, can solve the issue as the code is fairly well commented.


## Data sharing and dynamic geometry

Any moving objects, which are synchronized over multiple screens should use the shared data commit/update pattern.
Equalizer handles distribution of datastreams to clients. Data can be added/extracted from the stream by calling
```cpp
// only run on master
void commitSharedData(omega::SharedOStream& out)
{
    out << myPosition;
}
// only run on slaves!
void updateSharedData(omega::SharedIStream& in)
{
    in >> myPosition;
}
```

on a omegamodule class. We implemented this for all the relevant game classes using a listener pattern:
An interface is declared as 
```cpp
class SharedDataListener {
public:
    virtual void commitSharedData(omega::SharedOStream& out) = 0;
    virtual void updateSharedData(omega::SharedIStream& in) = 0;
};
```
and all classes which want to commit data to the stream inherit and implement this interface.
Then register the listening classes in you omega module and iteratively dispatch them. Note that the input must the same order as the output.

An example of synchronizing a dynamic gemeotry is the fence, which trails the bike in the Troen game.
First we create a Geometry with a vertex array and quad strip primitive set:

```cpp
void FenceView::initializeFence()
{
	m_coordinates = new osg::Vec3Array();
	m_coordinates->setDataVariance(osg::Object::DYNAMIC);

	m_geometry = new osg::Geometry();
	m_geometry->setVertexArray(m_coordinates);
	
	// use VBOs, not display lists. important for dynamic updates
	m_geometry->setUseDisplayList(false);

	m_drawArrays = new osg::DrawArrays(osg::PrimitiveSet::QUAD_STRIP, 0, 0);
	m_geometry->addPrimitiveSet(m_drawArrays);
}
```
In our update method, we add a new fence part, when the bike has moved a certain distance. When porting osg applications to omegalib, always make sure that all modified vertex arrays and geometry is dirtied, as else there will be crashes even if it runs fine under pure osg.
```cpp
void FenceView::addFencePart(osg::Vec3 currentPosition)
	// game fence part
	m_coordinates->push_back(currentPosition);
	m_coordinates->push_back(currentPosition + osg::Vec3(0,0,10));
    // trigger new boundary calculation
	m_geometry->dirtyBound();
	// very important to dirty vertex and attributes, as otherwise this will segfault in omegalib
    m_coordinates->dirty();
    // update the size of the draw array
	m_drawArrays->setCount(m_coordinates->size());
    // if its the master, cache the position to use in the commit data method
	if (omega::SystemManager::instance()->isMaster())
	{
		m_currentPositionCached = currentPosition;
		m_fenceUpdated = true;
	}
```

We call the *addFencePart* method in our update method, but only on the master. On the client, the method is called, when it receives new shared data:
```cpp
void FenceView::commitSharedData(omega::SharedOStream& out)
{
	out << m_fenceUpdated << m_currentPositionCached;
	// clear per frame states
	m_fenceUpdated = false;
}

void FenceView::updateSharedData(omega::SharedIStream& in)
{
	in >> m_fenceUpdated >>  m_currentPositionCached;
	if (m_fenceUpdated)
		addFencePart(m_currentPositionCached);
}
```



It is usually not necessary to sync the physics state, because the commit/update method is called every frame and the datalink in the Data Arena has a low latency. In Troen, we only synchronize the view transforms and do not execute the physics simulation on the child nodes at all. By doing this, we ensure that all nodes are in a consistent state and we do not have to worry about diverging physics states.

There can be situations however, where syncing the individual object transforms is not possible in a scalable manner, for example if a large particle system should be synced. In this case, the parameters of the particle system have to be synced and the simulation simultaneausly ran, setting random seeds uniformly.


