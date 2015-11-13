# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/home/fabian/Code/examples')

from omega import getDefaultCamera, setEventFunction, setUpdateFunction
from GeoLoader.GeometryFile import GeometryFile
from GeoLoader.DAEventHandler import DAEventHandler

modelFile = "/home/fabian/Code/examples/earth/mapquest_osm.earth"

cam = getDefaultCamera()
cam.setControllerEnabled(False)
cam.setPosition(Vector3(0, 0, 2) - cam.getHeadOffset())
cam.setNearFarZ(0.0001, 50)

geo = GeometryFile(modelFile)

geo.yRotClamp = 360
#geo.xRotClamp = 10
geo.xRotClamp = geo.zRotClamp = 0
geo.xMoveClamp = geo.yMoveClamp = geo.zMoveClamp = 1.5
geo.initialRotation = [-90,140,0]
geo.reset()

handler = DAEventHandler()

handler.yRotSensitivity = 0.1
handler.xMoveSensitivity = 0.0001
handler.yMoveSensitivity = 0.0001
handler.zMoveSensitivity = 0.001

handler.spaceNavMoveSensitivity = 3
handler.spaceNavRotSenstitivity = 0.001

handler.allowXRot = False
handler.allowZRot = False
handler.allowXMove = False

handler.addGeo(geo)

setEventFunction(handler.onEvent)
etUpdateFunction(handler.onUpdate)
