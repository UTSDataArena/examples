
# Building the scencegraph

The Geometry class provides a quick way of loading and interacting with models, however if you want to customize your models, materials etc., you have to build your own class for handling these models. Cyclops (or more precise the underlying OpenSceneGraph) uses a scenegraph to control the 3D geometry, states and transforms. 

A scene graph is a collection of nodes in a graph or tree structure. A tree node (in the overall tree structure of the scene graph) may have many children but often only a single parent, with the effect of a parent applied to all its child nodes; an operation performed on a group automatically propagates its effect to all of its members. Associating a geometrical transformation matrix at each group level and concatenating such matrices together is an efficient and natural way to process such operations. Commonly different shapes/objects are combined into a compound object that can then be moved, transformed, selected, etc. as easily as a single object.

In this tutorial, we are going to define our own geometry, build the scene graph and add different effects to objects.

### Step 1: Defining Geometry

In cyclops, simple geometry can be defined by using the ModelGeometry (add link) class. The defined Geometry maps to OpenGL primitive definitions, with a few abstractions. You can read up on this topic here: http://math.hws.edu/graphicsbook/c3/s1.html,  especially if you have never worked with computer graphics.
 In this tutorial, you will build and colorize a simple quad.
 

``` python
geom = ModelGeometry.create('quad')
v1 = geom.addVertex(Vector3(0, 0, 0))
v2 = geom.addVertex(Vector3(0, -1, 0))
v3 = geom.addVertex(Vector3(1, 0, 0))
v4 = geom.addVertex(Vector3(1, -1, 0))
geom.addPrimitive(PrimitiveType.TriangleStrip, 0, 4)
```
This snippet shows how to define a simple quad. The *ModelGeometry* class is actually a wrapper for OSG Geometry (insert) and defines a leaf-node of the scene graph (called geode in osg).In cyclops, all entities (visible objects) have to be registered in the scenemanager. This can be done using ```scenemanager.addModel()```, which stores a new ModelAsset in the scenemanager.

``` python
getSceneManager().addModel(geom)

quad = StaticObject.create('quad')
quad.setPosition(Vector3(0,2.5,-3))
```
To see the primitive, you have to add it to the root in the scene graph. Cyclops manages the root node in the scene-manager and a model can be added by creating a StaticObject (add link), and passing the name of the geometry. Cyclops stores a dictionary with a name to model mapping, and nodes can therefore generally be retrieved by their name. StaticObject derives from Entity (a cyclops class), which derives from SceneNode (an omega class), which both provide many functions to interact with scenegraph nodes. All entities are automatically added to the root node of the scenegraph, thereforeThe default camera is slightly tilted, therefore the object must be shifted into the camera field. Also the z-value (the depth) has to be lowered, because otherwise the quad overlaps exactly with the camera plane and will be clipped.

### Step 2: Adding instances

Now that the geometry has been defined, it can be used in any numbers of nodes. You can, for example, arrange quads in a circular way and add different colors:

``` python
self.colors = ["white", "green", "blue", "yellow", "black", "#ff00f4", "#00FFFF", "red"]
pi = 3.141592

for i in range(0, 8, 1):
    quad = StaticObject.create("quad")
    # arrange in a circular fashion in pi/4 intervals
    quad.setPosition(Vector3(sin(pi * i / 4.0) * 2,
                                 cos(pi * i / 4.0) * 2 + 2.5, -10))
    quad.setEffect('colored -e ' + self.colors[i])
```

Effects are a quick way to add custom appearance to objects and will be covered in another tutorial. 

(insert planes1.png)

### Step 3: interacting with the model

Using the left mouse button, you should be able to rotate the camera and look around. However, the model itself is static. In the last tutorial, we used the GeometryHandler class to provide interaction handlers for the incoming input events. This time, we did not use the Geometry class, however,  we can still use the Geometryhandlers by deriving our own class from BaseObject (pipelines.objects) and overriding the base methods.

``` python
class MyQuads(BaseObject):
    def __init__(self):
        BaseObject.__init__(self)
        #create geometry
        ...
        # create the root node of this object
        self.model = SceneNode.create("ParentNode")
        #change depth of parent instead of children
        self.model.setPosition(0,0,-10)
        self.quads = []
        
        for i in range(0, 8, 1):
            quad = StaticObject.create("quad")
            quad.setPosition(Vector3(sin(pi * i / 4.0) * 2,
                                         cos(pi * i / 4.0) * 2 , 0))
            quad.setEffect('colored -e ' + self.colors[i])
            self.quads.append(quad)
            self.model.addChild(quad)

```

Here, we added a parentNode to the quads, so that the object can be transformed as a whole, the pivot center of the rotation is therefore the center of "parentNode". Adding the quads as childs of the model will aplly every transform of the parent node to the child node. We set our self.model to the position (0,0,-10) and therefore all the children will be translated -10 along the z-axis additionally to their own transformations. We also store the quads seperately in a list for convenient access in the updateModel method.


```python
    def updateModel(self, newRotation, newPosition):
        self.model.rotate(Vector3(1, 0, 0), newRotation[0], Space.World)
        self.model.rotate(Vector3(0, 1, 0), newRotation[1], Space.World)
        self.model.rotate(Vector3(0, 0, 1), newRotation[2], Space.World)
        # add a quirky self rotation of the quads
        for quad in self.quads:
            quad.rotate(Vector3(0, 1, 0), newRotation[1] * 3, Space.World)
```

The function ```updateModel``` gets called for every new event from the geometryhandler and receives the new rotation and position. This example uses only the rotation to rotate the entire circle of quads around the pivot point in three degrees of freedom (euler angles). Additionally, a y-axis rotation is added for every subquad, to show the effect of manipulating child objects.

```python
# register object with handler
handler = GeometryHandler()
quad = MyQuads()
handler.addObject(quad)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
```
Finally, the handlers are initialized and registered, like in the first tutorial.


(insert planes2.png)

The complete source for the example lies in */local/examples/Tutorials/tut2/BuildSceneGraph.py* .


