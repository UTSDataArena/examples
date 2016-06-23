Welcome to the Data Arena VM tutorial series.
In the following tutorials we will show you, how to create, import and display cool models and bring them to the Data Arena.

Graphics programming experience is not a prerequisite, although it will help to have some understanding of the graphics pipeline.

# Technology stack

(maybe make a diagram of technology stack here?)


The Data Arena synchronizes its displays using a library called Equalizer to replicate low-level graphics commands over a network. However you will most probably not have to interact with it. The user builds graphical applications by using omegalib (insert link), cyclops and/or OpenSceneGraph. Omegalib is middleware designed to ease the development of applications for virtual reality (VR) and immersive display environments and can integrate a variety of other frameworks. We use OpenSceneGraph (insert link), a powerful graphics rendering library, to render our graphics. However, OpenSceneGraph is also a fairly complex library with a steep learning curve. Therefore, cyclops (insert link), a high-level API for osg is used to do common graphic operations in the Data Arena. The Data Arena also provides custom classes to handle standard use-cases and to ease the first steps.

# Getting Started
The Data Arena VM comes with all the software needed to display things in the Data Arena.
For this tutorial, we will mostly interact with scripts inside the "/local/examples/" folder, which contains the examples of this tutorial(s) and the custom handlers (in the pipelines folder). 

So lets get started and build our first immersive application!

# Cube Tutorial
The hello world program of the graphics world is displaying a simple object, such as a cube. Before being able to display anything, you have to have a model of a cube first, of course. Creating and exporting models will be covered in the next tutorial, for now, take the "box.obj" model from the "examples/box" folder. Wavefront (.obj) models are a popular format for exchanging 3d models between different applications. They contain the definition of the geometry, colors and many optional definitions. Fortunately, we don't have to parse this model by ourselves but can use a model loader, which is part of the osg package. The "Geometry" class takes care of loading the model and adding it to the scenegraph (more on that later).

The following is a minimal working example:
```python
import sys
sys.path.append('/local/examples')

from pipelines.objects import Geometry
from pipelines.handler import GeometryHandler 

fileToLoad = "/local/examples/box/box.obj"

geo = Geometry(fileToLoad)

handler = GeometryHandler()
handler.initialCamPosition = [0, 0, 5]
handler.addGeo(geo)
```

The code above adds the examples folder to the system path, so the pipelines are importable. 
Then, by creating an Geometry object and giving it the path to the model, the box.obj model is loaded, added to the scene and its material is set. Have a look at "objects.py" (link to geometry docs or source), to see what exactly is going on.

Then a GeometryHandler is instanced and the geometry is registered with the addGeo() method. This step ensures, that the camera is focused on the center of the model. Before adding geometry, set the initial camera position to have a higher z value, so the camera looks from above onto the object and is not too close.

(embed box1 image)

To add another box to the scene, you can load the box in a new Geometry, set its initial position to a different position and register it to the GeometryHandler. Also set the initial camera position to the middle of both cubes.

``` python
#update the initial camera position
handler.initialCamPosition = [1, 0, 5] 
#add new box
geo2 = Geometry(fileToLoad)
geo2.initialPosition = [2,0,0]
handler.addGeo(geo2)
```

(embed box2 image)

Now both boxes are displayed, but we can't interact with them yet. The GeometryHandler class contains configurable interaction handlers, which let you control the model using different input devices (mouse, ps4 controller, space navigator). To use the event handlers, they have to be registered in omegalib.

``` python
setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
```
The setEventFunction (add link) passes through all input events to the handler's onEvent function, the setUpdateFunction (add link) registers a script function to be called before each frame is rendered.
Now the boxes can be rotate in the scene. The interaction handler provides several ways to constrain the movement of the camera and of the object, which are displayed in the console.
When pressing "m", the mode can be toggled between object mode to camera mode. You can use object mode to rotate and translate the object and camera mode to orient yourself in the space in a first person way.

(embed box3 image)


In the next tutorial, you will learn how to apply simple materials to objects.


