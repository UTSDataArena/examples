# Advanced omegalib/osg applications

Building visualizations with cyclops in python can produce stunning results and provides tools for many use cases, however there are certain applications which cannot be built with cyclops/python (without extending the cyclops c++ classes).
The underlying framework OpenSceneGraph is a powerful general purpose computer graphics library, which omegalib/cyclops uses to render computer graphics distributed across multiple displays.
Reasons for programming in osg/omegalib in c++ could be
* You already have an existing application application using osg that you want to port to a multi-display setup in omegalib
* Your application requires a large amount of data processing, dynamic geometry or special effects
* You want to use third party c++ libraries, such as physics or sound engines
* You want to use any methods of osg which are not accesible in cyclops


This tutorial assumes that you already have knowledge of programming in osg. If not, there are many good resources on the internet to learn programming the OpenSceneGraph, for example, the OpenSceneGraph Beginner's Guide (http://ahux.narod.ru/olderfiles/1/OpenSceneGraph.3.0.Beginners.Guide-3208.pdf) will get you started and contains many good examples. Going further, the OpenSceneGraph Cookbook (https://www.packtpub.com/game-development/openscenegraph-3-cookbook) provides recipes for many advanced topics.

### Integration of osg and omegalib

Omegalib comes with support for openscenegraph as its rendering system in form of the omegaOsg module. It is important to know, how osg is actually integrated into omegalib and how rendering on distributed nodes work, to be able to efficiently develop applications in omegalib. Unfortunately, there is no official documentation of the omegaOsg module, which leaves programmers with only the source code to work with. Luckily, the binding code between osg and omegalib is rather small and not too complex.

(insert diagramomegaOsg.png)

The omegaOsg module is a omegalib module which contains a osg::Node (the root) and registers a custom renderpass to the omegalib library. On each frame, the equalizer displaysystem calls the render method (on all nodes) of the renderpass class. Internally, the osgmodule copies over all transforms and properties of the omegalib camera to a osg::Camera and then the sceneview class performs the culling and rendering of the scenegraph. It is important to know, that no geometry is shared among nodes (in fact not even transforms are shared), the distributed nodes all run the same program and the renderloop execution is synced. Therefore transforms or dynamic geometry might have be synced by yourself. We will elaborate on this topic later again.


# Building a standalone application

All examples, which come with the omegalib, are embedded into its environment and can only be built by invoking the general omegalib build command. If you are developing a larger application, this is really inconvenient and you probably want to seperate your application binaries, data, etc. from the binaries of omegalib. The omegalib wiki has a page on building standalone applications (https://github.com/uic-evl/omegalib/wiki/NewApplication), however it does not cover all the aspects needed to get a running environment.

Omegalib assumes that libraries are relative to the current binary runpath. If you are not running the application binary from omegalib/build/bin, however, the libraries needed will not be found. 
You can add the directory of the binaries to the datamanager. In the cmakelists, add in a definition which points to the directory:
```
add_definitions(-DOMEGALIB_BIN_DIR="${Omegalib_DIR}/bin")
```
and in your code, before calling omain add the directory to the data manager so the libraries can be dynamically loaded:
```c++
omega::DataManager* dataManager = omega::SystemManager::instance()->getDataManager();
dataManager->addSource(new omega::FilesystemDataSource(OMEGALIB_BIN_DIR));
```

Next, we show a minimal example for building a standalone Application using omegalib. First, we declare our Module class. The class will be constructed by omegalib. The constructor creates a new osgmodule and reigsters it in the omega moduleservices. The actual initialization of the scene is done in initialize, which is called by omegalib on the first iteration of the renderloop.

```c++
#include <osgDB/ReadFile>
#include <omega.h>
#include <omegaOsg/omegaOsg.h>

omega::String sModelName;
///////////////////////////////////////////////////////////////////////////////
class MinimalExample: public omega::EngineModule
{
public:
    MinimalExample(): EngineModule("MinimalExample")
    {
        myOsg = new omegaOsg::OsgModule::instance();
    }
    virtual void initialize();
private:
    omegaOsg::OsgModule* myOsg;
};
```

Our initialize method simply loads a node file from the disk, using a modelname passed in over the commandline. 
Omegalib initiliazes all its state in the module initiliaze traversal, whichs initializes equalizer, omgealib, omicron, etc. 
Make sure that any calls with references to omegalib objects are invoked in the initialize method at the earliest. 

```c++
void MinimalExample::initialize()
{
    // The node containing the scene
    osg::Node* node = NULL;

    omega::String path;
    if(omega::DataManager::findFile(sModelName, path)) {
        node = osgDB::readNodeFile(path);
        if (node == NULL) {
            omega::ofwarn("!Failed to load model: %1% (unsupported file format or corrupted data)", %path); 
            return;
        }
    }
    // attach any global state (shaders, lights, etc.) to this node\
    myOsg->setRootNode(node);
}
```
Finally, the main methods creates a omegalib application, reads from the commandline and then executes the main omegalib loop.
```c++
///////////////////////////////////////////////////////////////////////////////
// Application entry point
int main(int argc, char** argv)
{
    omega::Application<MinimalExample> app("minimalExample");
    omega::oargs().newNamedString(':', "model", "model", "The osg model to load", sModelName);
    return omega::omain(app, argc, argv);
}
```

### Overriding omegalib file loaders

Omegalib registers custom file loaders, which in some cases override the standard osg plugins. Sometimes, this can lead to unexpected behaviour: for example the tga of omegalib does not implement the full tga standard and loading images with 24bpp, which loaded fine with the osgdb_tga plugin will not work anymore. To use a certain osg loader, you have two options: load data/textures/nodes before the omegalib ``omain`` call or manually remove loaders from registry. The first method is preferred, if you only need to load files once and can do this before starting the actual application. If not, the second method provides a (little bit hacky) workaround.

To remove a loader from the osgDB registry, first store the filepaths before running ``omain``:
```c++
for (auto libPath : osgDB::Registry::instance()->getLibraryFilePathList ()) 
{
        _storedLibPaths += libPath + ":";
}
```
storedLibPaths should then contain the correct directories of plugins (the standard osg directories), you want to load.
When running omain, the omegaOsg initiliaze method will set the plugin library searchpath automatically to a directory containing the loaders you don't want to use.
To revert this, reset the osgDB::Registry library search path to its original path. 
Then, remove the reader writer which is giving troubles from the registry, this will cause a reload on invocation using the plugins in the correct path
```c++
// The omegaOsg instance() method initiliazes it and configures its libpaths, so it is safe 
// to revert these libpaths in our initialize method
MinimalExample::initialize(){
    osgDB::Registry* reg = osgDB::Registry::instance();

    reg->setLibraryFilePathList(_storedLibPaths);
    osgDB::Registry::instance()->removeReaderWriter(
        osgDB::Registry::instance()->getReaderWriterForExtension("tga"));
        
    // now you can load your tga files, and they will be correctly loaded by the osg loader plugin
```

### Debugging your application

Debugging computer graphics application can be quite hard, as the errors can manifest themselves as visual artefacts or other errors, which are quite hard to trace down.
Setting the notify and log level to debug can help tracing down many errors:
set the `OSG_NOTIFY_LEVEL=DEBUG`  in your environment for detailed osg debug messages
pass the `--log v` flag to your application, for omegalib debug messages

Crashes which happen during the initiliaze call can sometimes be hard to debug, as no actual debug messages are displayed. Shifting the method call into your gameloop to test assumptions often helps in getting more useful error messages.

When debugging an application over multiple nodes in equalizer, getting debug traces can be tricky. One way to get information about segfaults is to have a custom launcher script for children in the .cfg file and log the stack trace to a a file: 
Set the nodelauncher in your .cfg file to a custom script: 
```
nodeLauncher = "ssh -n %h startTroenSlave.sh %d %c"
```
 startTroenSlave. sh:
```
D=$1
C=$2
cd $D
... # set other environment variables
export LD_LIBRARY_PATH=$D:${D}/osg:${D}/osg/osgPlugins-3.3.0:$LD_LIBRARY_PATH

# -r is for remote log
gdb -x gdbcommand.txt --args  $C -r --log v  $*
```


gdbcommand.txt:
```
set logging file gdb.txt
set logging on
run
bt
```



### Gotchas when using omegaOsg
Although omegaOsg allows the usage of most osg concepts, some osg features do not work when used in omegalib
- rendering masks are not processed by omegaOsg, therefore all geometry will be displayed twice if you are using two cameras with different camera masks.  If you experience similar artifacts as in figure 1 (insert flickering.png), you might have probably have multiple cameras rendering the scene with either ignored camera mask settings, culling settings or render order settings.
- You do not have access to the actual osg rendering camera before rendering. There is however a framefinished callback, which gives you access to the rendering internals


# Hands On: Integrating a game into omegalib 

In this section, we will show a few common problems arising, when integrating highly interactive applications such as games. We will show the solution to these problems in the context of integrating a game using osg and bullet physics, called Troen. For source reference and more in-depth examples of integrating a fairly advanced osg application into omegalib, you can find the source of the game on [github](https://github.com/MaxReimann/Troen).

(insert troen-2window.png)

screenshot of the game running across two windows

### Setting transforms on omega cameras:
The main interaction between omegalib and osg concerns the setting and updating of cameras. When implementing or porting an application with dynamic cameras, which can move around, rotate/orbit, etc. care must be taken to apply the correct transform.
In osg, cameras can be part of the scene graph in lower levels. When their reference frame is set to RELATIVE_RF, they will reference all underlying geomertry from a relative coordinate frame. However omega cameras are commonly set in an absolute reference frame. When calculating transforms, e.g. taking the output of a osg camera manipulator, care must be taken to convert the local transform into the world transform. 

An example for such a transformation is the updateCamera method of the nodetrackermanipulator, which orbits around a tracked node and sets the camera in every frame. The nodetrackermanipulator computes a center and rotation around the tracked node and when updating the camera, it uses the inverse of this transform to set its lookat:

```c++
void NodeTrackerManipulator::updateCamera(osg::Camera& camera) 
{ 
	osg::Vec3d eye, center, up, unused;
    osg::Matrixd invMatrix = getInverseMatrix();
	invMatrix.getLookAt(eye, center, up);
	camera.setViewMatrixAsLookAt(eye,center,up);
}
```
The *omega::Camera* also has a lookat method, however, if you update the *omega::Camera* by using its lookat method, it will produce weird, incorrect rotations, which are a symptom of the wrong coordinate frame of the center vector: The coordinate frame of the calculated center vector is in the camera view space but should really be in the world space.

```c++
void NodeTrackerManipulator::updateOmegaCamera(omega::Camera *cam){
    osg::Vec3d eye, unused_center, up;

    // call same method, that osg internally uses for its camera updates
    osg::Matrixd invMatrix = getInverseMatrix();
	invMatrix.getLookAt(eye, unused_center, up);

   	osg::NodePath nodePath;
   	//get the path from the tracked node to the top level element
   	getTrackNodePath().getNodePath(nodePath);
   	//compute a transform from the tracked node space to world space
    osg::Matrixd localToWorld = osg::computeLocalToWorld(nodePath, true);
    // apply this transformation to the cameramanipulator center
    // this is normally the tracked node center, but might be panned
    osg::Vec3d worldCenter = _center * localToWorld;

    omega::Vector3f oCenterVec = OSGVEC3_OMEGA(worldCenter);
    // set the lookat of omega camera
    //order is important here, setting lookat before position 
    // will result in choppy camera rotation
    cam->setPosition( OSGVEC3_OMEGA(eye) );
    cam->lookAt(oCenterVec, OSGVEC3_OMEGA(up) );     
}
```

### Executing pre-render cameras

In osg, cameras can have different render orders: Pre-render, normal, and post-render.
Pre-render cameras are often used, to render a certain effect into a texture, which are then used in the actual rendering of the scene. A common use case is rendering reflections on surfaces.

In our game, we want to render a very shiny surface. A pre-render camera is used, to render the scene with a flipped z-transform:

(todo: extract and insert snapshot from presentation)

Our camera therefore moves with the main camera and its position has to be updated accordingly. Setting the transformation of the reflection camera at the right time is crucial, because setting it too late will result in the reflection lagging one frame behind and too early will result in the main camera not being updated with the new transform yet. A hacky method  could be to directly copy over the main camera transform to the reflection camera, when it is set in the cameramanipulator. However, this could break as soon as we have other methods influencing the camera position: imagine a method setting the field of view dynamically or a method preventing cameras flying into obstacles. Another problem is, that in omega multiple windows can be created on one machine, each update method is therefore executed once for each camera.If you have two windows, you will probably see constantly switching reflections between the windows, because the transform is applied to the wrong reflection camera. What we actually want is to have a camera callback executed right before the reflection camera is rendered. 

In osg, the cull traverse decides what objects to render and what to cull away. The Cullvisitor actually computes the correct transformation of each node and pushes objects into the the draw stage, which is executed after the Cullvisitor has visited all nodes. Therefore, the CullCallback is the latest point, we can influence a nodes transform before it is rendered. However the cullcallback is executed after the node transforms have already been pushed into the render stage.If we would therefore execute the cullcallback directly on the camera, we would not see any positional change. We must therefore set the cullcallback on a node above the camera (we named it cameragroup) and then access its child:

```c++
class CUpdateCameraCallback : public osg::NodeCallback
{
public:	
	CUpdateCameraCallback() : NodeCallback(){}
	void operator()(osg::Node *node, osg::NodeVisitor *nv)
	{
	    // only execute this callback if in the culling stage
		if (nv->getVisitorType() == osg::NodeVisitor::CULL_VISITOR)
		{
		    // the camera is the only child of the camera group
			osg::Camera	*camera = dynamic_cast<osg::Camera *>(node->asGroup()->getChild(0));
			// The cullvisitor holds information about the current (main) camera
			osgUtil::CullVisitor* cv = static_cast<osgUtil::CullVisitor*>(nv);

			if (camera != NULL)
			{
			    // copy over the transforms of the main camera
				camera->setProjectionMatrix(cv->getCurrentCamera()->getProjectionMatrix() );
				camera->setViewMatrix(cv->getCurrentCamera()->getViewMatrix());
				// set the eye point in the shader
				g_cameraEyeU->set(cv->getEyePoint());
			}
		}
		this->traverse(node, nv);
	}
};
```

Now we show , how to set up the camera correctly:
```c++
	cameraGroup = new osg::Group();
	m_reflectionCamera = new osg::Camera();
	reflectionTransform = new osg::MatrixTransform();
	
	cameraGroup->addChild(m_reflectionCamera);
	m_reflectionCamera->addChild(reflectionTransform);

    m_reflectionCamera->setClearMask(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);
    // render the camera before the main camera
	m_reflectionCamera->setRenderOrder(osg::Camera::PRE_RENDER);
	// write into a frame buffer later used as texture
	m_reflectionCamera->setRenderTargetImplementation(osg::Camera::FRAME_BUFFER_OBJECT);
	// prevent near clipping
	m_reflectionCamera->setComputeNearFarMode(osg::CullSettings::DO_NOT_COMPUTE_NEAR_FAR);
	// calculate all transforms in world space
	m_reflectionCamera->setReferenceFrame(osg::Transform::ABSOLUTE_RF);
	// set the viewport to the size of the texture
	m_reflectionCamera->setViewport(0, 0, texSize, texSize);
	m_reflectionCamera->setClearDepth(1.0);

    //Important: set our cull callback on the cameragroup, not the camera itself
	m_cameraGroupCallback = new CUpdateCameraCallback();
	cameraGroup->setCullCallback(m_cameraGroupCallback);
```

Calculating the actual reflection does not need any extra adjustements for distributed rendering, but is shown here for reference:
```c++
    // add a clipping plane, to clip everything below z=0.0. 
    //beware, that vec4(a,b,c,d) is a plane equation with a,b,c the plane normal and d the plane height
	m_reflectionClipPlane = new osg::ClipPlane(0, osg::Vec4d(0.0, 0.0, 1.0, 0.0));
	m_reflectionClipNode = new osg::ClipNode;
	m_reflectionClipNode->addClipPlane(m_reflectionClipPlane);
	reflectionTransform->addChild(m_reflectionClipNode);
	// mirror the scene along the z axis
	reflectionTransform->setMatrix(osg::Matrix::scale(1.0, 1.0, -1.0));

    // render the reflection camera into a texture
	osg::ref_ptr<osg::Texture2D> texture = new osg::Texture2D();
	texture->setTextureSize(texSize, texSize);
	m_reflectionCamera->attach((osg::Camera::BufferComponent) osg::Camera::COLOR_BUFFER0, texture);

    osg::StateSet *cameraState = m_reflectionCamera->getOrCreateStateSet();
	cameraState->setMode(GL_CULL_FACE, osg::StateAttribute::OFF | osg::StateAttribute::OVERRIDE);
	// Set reflection textures
	osg::StateSet* floorStateSet = reflectingSurface->getOrCreateStateSet();
	floorStateSet->setTextureAttributeAndModes(0, texture, osg::StateAttribute::ON);
```
The complete reflection code is found in source/view/reflection.cpp and shaders/grid.(vert|frag)

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
```c++
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
```c++
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

```c++
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
```c++
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
```c++
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


