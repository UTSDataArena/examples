# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import setEventFunction, setUpdateFunction
from GeoLoader.GeometryFile import GeometryFile
from GeoLoader.DAEventHandler import DAEventHandler

cave = GeometryFile("/da/proj/paulBourke/weld/take1.obj")
cave.initialRotation = [-15, 170, -175]
cave.initialPosition = [0.05, 0, -0.9]
cave.reset()

handler = DAEventHandler()
handler.cameraControl = True

handler.allowZRot = False
handler.allowXMove = handler.allowYMove = False

handler.addGeo(cave)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
