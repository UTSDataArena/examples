import os.path, sys
basePath = os.path.dirname(os.path.abspath(__file__)) # for current dir of file
modulePath = os.path.dirname(os.path.dirname(basePath)) # for GeoLoader packages - '/local/examples'
sys.path.append(modulePath) 


from pipelines.objects import BaseObject
from pipelines.handler import GeometryHandler

from cyclops import *
from omega import SceneNode, Space

from math import sin, cos


class MyQuads(BaseObject):

    def __init__(self):
        BaseObject.__init__(self)


        geom = ModelGeometry.create('quad')
        v1 = geom.addVertex(Vector3(0, 0, 0))
        v2 = geom.addVertex(Vector3(0, -1, 0))
        v3 = geom.addVertex(Vector3(1, 0, 0))
        v4 = geom.addVertex(Vector3(1, -1, 0))
        geom.addPrimitive(PrimitiveType.TriangleStrip, 0, 4)

        getSceneManager().addModel(geom)

        pi = 3.141592

        self.model = SceneNode.create("ParentNode")
        self.model.setPosition(0,0,-10)
        self.quads = []
        self.colors = ["white", "green", "blue", "yellow", "black", "#ff00f4", "#00FFFF", "red"]

        for i in range(0, 8, 1):
            quad = StaticObject.create("quad")
            quad.setPosition(Vector3(sin(2 * pi * i / 8.0) * 2,
                                         cos(2 * pi * i / 8.0) * 2 , 0))
            quad.setEffect('colored -e ' + self.colors[i])
            self.quads.append(quad)
            # set this to render the object from both sides
            quad.getMaterial().setDoubleFace(True)
            self.model.addChild(quad)



    def updateModel(self, newRotation, newPosition):
        self.model.rotate(Vector3(1, 0, 0), newRotation[0], Space.World)
        self.model.rotate(Vector3(0, 1, 0), newRotation[1], Space.World)
        self.model.rotate(Vector3(0, 0, 1), newRotation[2], Space.World)

        for quad in self.quads:
            quad.rotate(Vector3(0, 1, 0), newRotation[1] * 3, Space.World)


handler = GeometryHandler()
quad = MyQuads()
handler.addObject(quad)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)


