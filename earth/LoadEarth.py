# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import setEventFunction, setUpdateFunction
from GeoLoader.GeometryFile import GeometryFile
from GeoLoader.DAEventHandler import DAEventHandler

modelFile = "/local/examples/earth/mapquest_osm.earth"

geo = GeometryFile(modelFile)

geo.yRotClamp = 360
#geo.xRotClamp = 10
geo.xRotClamp = geo.zRotClamp = 0
geo.xMoveClamp = geo.yMoveClamp = geo.zMoveClamp = 1.5
geo.initialRotation = [-90, 140, 0]
geo.reset()

handler = DAEventHandler()
handler.initialCamPosition = [0, 0, 2]
handler.resetCamera()

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
setUpdateFunction(handler.onUpdate)
