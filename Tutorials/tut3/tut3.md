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

## View Manipulators

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


