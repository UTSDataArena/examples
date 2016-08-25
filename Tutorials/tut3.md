# Defining your own interactions

In this tutorial you will learn
* how to implement custom interaction handlers
* how to export 3D models from a modelling software and import them to omegalib
* how to display text 

Suppose you want to visualize a portion of a city and enable the user to query information about particular buildings by clicking on them.
In this tutorial you will build and export a 3d model of a building block, assign values to the building and define interaction handlers to process click events and then display information about the building in a text-over block.


### Building and exporting the model

Fire up your 3D modelling tool of choice, and start building your model. This tutorial uses Blender, but the workflow is similar to other 3D modelling tools.

A small building block model can be made, by importing a highly detailed map section, covering the buildings with polygons and extruding them. We have built a simple model of the UTS:

(insert blender.png)

Now, the model has to be exported to omegalib. The underlying OpenSceneGraph can understand many common formats (.obj, .3ds, .ply, ...), however the most convinient way is to export into .osgt, the native osg format. This format explicitly defines the scenegraph is easibly readable for humans. Check http://trac.openscenegraph.org/projects/osg//wiki/Community/Plugins for available exporters, there are exporters for 3D Studio Max, Maya and Blender (plugins for other model packages might exist elsewhere). The best plugin for Blender is maintained under https://github.com/cedricpinson/osgexport, use this to export your scene into .osgt, the default settings for the export are appropriate.

Now have a look at the osgt file to grasp, what the scenegraph looks like. There is a root object and child objects. Depending on the object type, it has material, vertex and/or texture data assigned. Note that in Blender, only the materials set for the Blender renderer (not cycles) are exported. You can import and show the pieces of your model in python:

``` python
modelInfo = ModelInfo()
modelInfo.name = "UTS"
modelInfo.path = "UTS.osgt"
modelInfo.size = 65.0
#its important to not use the optimizer, 
# so that all seperately defined objects stay seperate
modelInfo.optimize = False
# loads model, but does not attach it yet
getSceneManager().loadModel(modelInfo)
# loads model by name, and attaches it to scene
model = StaticObject.create("UTS")
#print out all objects defined in the model
for pieceName in  model.listPieces("Root"):
    print pieceName
```
When executing this code, the diplayed model should look similar to this:
(insert cyclops1.png)

The camera is oriented horizontally to the model and can not be moved.
We want to the camera a more interesting camera angle and position. Trying out different positions from python
is a lot of tiring manual work and therefore we want to use the camera view transformation defined in our modelling program. 
To get this, find out the name of your camera in Blender (or other modelling program) and check, if this name is present as a node in the .osgt file (which it should be). 

To get the position, extract the node from the model graph:
``` python
cam = model.getPiece("Root/Camera")
print cam.getPosition()
```
The getPiece method returns an ``Entity``, which is still anchored in the scenegraph, and we can retrieve its position.
The next thing we need is the camera lookat and up vector. We will avoid having to calculate a orientation to lookat transformation by setting the camera lookat point ourself. In Blender (or other program), create an Empty at the center position of the camera and set the camera to its parent. By doing this, the Empty, which you can call the CameraFocus, will always stay centered in the camera view. Now export the scene again and retrieve the camerafocus position by 

``` python
focus = cam.getPiece("CameraFocus")
worldfocusPos = cam.convertLocalToWorldPosition( focus.getPosition() )
```

Note that the focus position is local to its parent and has to be transformed into world space.



You will use these positions in the next step.

### View Manipulators

In previous tutorials, we have used the ``GeometryHandler`` class to walk though the model in a first-person style. 
In this tutorial, we want to be able to rotate, pan and zoom the model similar to the 3D view in modelling programs.
The Data Arena version of cyclops offers a ``ManipulatorController`` class, which makes it possible to use  *osg::CameraManipulator*  with omegalib cameras. 

Create a class which instantiates both a ``ManipulatorController`` and a ``TerrainManipulator`` and set the ManipulatorController to use the TerrainManipulator. 

```TerrainManipulator``` is a wrapper around ``osg::TerrainManipulator`` and defines zooming, panning and rotating around terrains with horizontal terrain zooming.
Other currently implemented Manipulators are: ``OrbitManipulator`` and ``NodeTrackerManipulator``.

``` python
class CameraHandler:
    def __init__(self):
        # controller for camera manipulators
        self.camManipController = CameraManipulator.create()
        # the actual camera manipulator
        self.manipulator = TerrainManipulator.create()
        self.camManipController.setManipulator(self.manipulator)

    def onEvent(self):
        """Callback for omegalib to register with `setEventFunction`."""
        self.camManipController.onEvent(getEvent())
```

Now, we can instatiate the CameraHandler and set it to handle our model:
``` python
...
camManipulator = CameraHandler()
camManipulator.setCameraHome(cam.getPosition(), worldFocusPos)

setEventFunction(camManipulator.onEvent)
```
Rotating, panning and zooming should now be possible.

By default, the manipulators use the mouse.Using different input devices is also possible, by using a different ``EventHandler``. EventHandlers transform input of various devices into mouse events for osg. To use a playstation controller, for instance, add a ```MyControllerAdapter``` in the constructor of the CameraHandler.
``` python
    def __init__(self):
        ...
        self.eventAdapter = MyControllerAdapter(self.manipulator)
        self.camManipController.setEventAdapter(self.eventAdapter)
        
        def onUpdate(self, frame, time, dt):
            if self.eventAdapter != None:
                self.eventAdapter.onUpdate(self.camManipController)
...
setUpdateFunction(camManipulator.onUpdate)
```

The onUpdate function ensures smooth transformation for controller events.

# Selecting models in the view

To enable the user to interact with the model, we want to him to to be able to hover over model parts, make selections and get visual feedback. We want to color a node if the cursor is hover over it:
(insert cyclops2.png)

The first step is to check if our mouse is hovering over a model.
Define a new class called SceneHandler, and add a onEventMethod. Modularlizing your code in camerahandlers, scenehandlers, modelcontrollers, etc.. is always a good idea to encourage loose coupling and reusability of components.

```python
class SceneHandler:
    def__init__(self):
        pass
    
    def onEvent(self):
        e = getEvent()
        if(e.getServiceType() == ServiceType.Pointer or e.getServiceType() == ServiceType.Wand):
            r = getRayFromEvent(e)

            # Button mappings are different when using wand or mouse
            confirmButton = EventFlags.Button1
            if(e.getServiceType() == ServiceType.Wand): confirmButton = EventFlags.Button5
            
            if(r[0]): 
                # When the confirm button is pressed:
                if(e.isButtonDown(confirmButton)):
                    self.mouseClickPos = e.getPosition()
                    querySceneRay(r[1], r[2], self.onClicked, QueryFlags.QuerySort | QueryFlags.QueryFirst)
                else:
                    querySceneRay(r[1], r[2], self.colorHovered, QueryFlags.QuerySort | QueryFlags.QueryFirst)
```

Cyclops offers functions which makes this quite easy:
- getRayFromEvent: returns a ray which has its startpoint set at the camera eye position and the direction towards the mouse pointer 
- querySceneRay: Makes intersection tests between the ray and all nodes and executing a callback for every node that is returned (hit). We sort the scene from shortest to longest distance and return closest node. Only nodes, which are set as *selectable* will be queried.

Until now, we only have one root ``omega::SceneNode`` in the scene. Note that this is a different type of node than ``osg::Node``. To make different parts of the model selectable, all seperate parts of the model have to be extracted into a SceneNode. 
Using this selection method is most useful, if there is a pointer device (mouse or wand) available.

Wrap the model loading part into a new class called *ModelController* and add a new method  *setSelectableParts*, which is called after loading in the constructor:
``` python
#in class ModelController:
    def setSelectableParts(self):    
        self.selectableNodes = []
        self.model.setSelectable(False)
        for pieceName in self.model.listPieces("Root"):
            if pieceName == "Camera": #dont extract the camera yet
                continue
            mod = self.model.getPiece("Root/" + pieceName)
            if pieceName.startswith("cb"):
                if mod != None:
                    mod.setSelectable(True)
                    self.selectableNodes.append(mod)
            else:
                mod.setSelectable(False)
```
In Blender, we have named every building using the "CBxx" naming. We only want to make UTS building nodes selectable, so we set everything which does not start with "cb" to non-selectable. We also don't want to extract the camera, as we do this later to query its position/lookat and a piece can only be extracted once because a new scenenode is created and maintained using its name.

Next, we define the callback to be called, when there is a event (except for mouse clicks):
```python
    def colorHovered(self, node, dist):
        if node != None:
            for n in self.modelController.getSelectableNodes():
                if n.getName() == node.getName():
                    n.getMaterial().setColor(Color(1.0,1.0,1.0,1.0), Color(0.2, 0.2,0.2, 0.2))
                else:
                    n.getMaterial().setColor(Color(0.2,0.2,0.2,1.0), Color(0.0, 0.0,0.0, 0.0))
        else:
            for n in self.modelController.getSelectableNodes():
                n.getMaterial().setColor(Color(0.2,0.2,0.2,1.0), Color(0.0, 0.0,0.0, 0.0))
```

The *querySceneRay* returns a node which was found and its distance. The node can also be None, if nothing was found.
We set the model part's material to a bright white color, if it is under the cursor and all other buildings to a more darkish color. If no node was found, set all parts to the same darkish color.
Now you should be able to see you selections by hovering over buildings.

# Displaying Information on the UI
To complete our example, it would be nice to show information about the buildings when clicked. Getting information into the visualization is always application specific, but one simple way to get in information is to define a json dictionary which maps node names to information.

Displaying the height of the building will suffice for this example:
```json
{
 "buildings":{
         "cb1" : {"height": 150},
         "cb2" : {"height": 20},
         "cb3" : {"height": 15},
         "cb4" : {"height": 15},
         "cb5" : {"height": 20},
         "cb6" : {"height": 60},
         "cb10" : {"height": 35},
         "cb11" : {"height": 40}
        }
}
```

Omegalib offers some UI functionality, which makes it easy to define 2D widgets, which are rendered infront of the scene.

```python
class SceneHandler:
    def __init__(self, modelController):
        self.modelController = modelController

        self.ui = UiModule.createAndInitialize()
        self.wf = self.ui.getWidgetFactory()
        self.uiroot = self.ui.getUi()

        containerSize = Vector2(300, 100)
        self.container = self.wf.createContainer('container', self.uiroot, ContainerLayout.LayoutVertical)
        self.container.setAutosize(False)
        self.container.setSize(containerSize)

        self.label = self.makeLabel("label1")
        self.label2 = self.makeLabel("label2")
        self.lastMousePos = None
        
        with open('buildinginfo.json') as data_file:    
            self.buildinginfo = json.load(data_file)
            
    def makeLabel(self, name):
        label = self.wf.createLabel(name, self.container, '')
        label.setAutosize(True)
        label.setStyle('font: fonts/arial.ttf 30; color: white; alpha: 1.0;')
        label.setStyleValue('align', 'middle-left') 
        label.setVisible(False)
        return label
```

The UI works similar to other UI frameworks. A [Container](https://github.com/uic-evl/omegalib/wiki/Container) is needed to hold [Widgets](https://github.com/uic-evl/omegalib/wiki/Widget), such as [Labels](https://github.com/uic-evl/omegalib/wiki/Label), [Buttons](https://github.com/uic-evl/omegalib/wiki/Button) and [Sliders](https://github.com/uic-evl/omegalib/wiki/Slider). There is no textwrap in omegalib, so for every line, a new label has to be created.

The `json` library is used, to convert the json file into a python dictionary.

The last step is to actually display the text, when the building is clicked. We define the querySceneRay callback for mousedown button events:

```python
    def onClicked(self, node, dist):
        if node != None:
            onLeft = 1 if (getDisplayPixelSize()[0] / 2.0 > self.mouseClickPos[0] ) else -1
            pos = self.mouseClickPos + onLeft * Vector3(150, 0, 0)
            self.updateTextInfo(node)
            self.container.setCenter(pos)
            self.container.setVisible(True)
        else:
            self.container.setVisible(False)           
    
    def updateTextInfo(self, selectedNode):
        if self.buildinginfo["buildings"].has_key(selectedNode.getName()):
            building = self.buildinginfo["buildings"][selectedNode.getName()]
            self.label.setText("Building: " + selectedNode.getName())
            self.label2.setText("Height: " +  str(building["height"]) + "m")
        else:
            self.label.setText("Building: N.A")
            self.label2.setText("Height: N.A")
```
We position the text box to the left or right depending on the click position, to avoid the text box reaching out of the window bounds.


(insert cyclops3.png)


And thats it, you got a nice DataViz application running, ready to be deployed in the Data Arena.
The full code (with some additions) is available at "/local/examples/Tutorials/tut3/CustomInteraction.py"



