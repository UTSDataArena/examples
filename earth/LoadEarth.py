# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/home/fabian/Code/examples')

from omega import setEventFunction, setUpdateFunction
from GeoLoader.GeometryFile import GeometryFile
from GeoLoader.DAEventHandler import DAEventHandler

modelFile = "/home/fabian/Code/examples/earth/mapquest_osm.earth"

geo = GeometryFile(modelFile)

geo.yRotClamp = 360
geo.xRotClamp = geo.zRotClamp = 0
geo.xMoveClamp = geo.yMoveClamp = geo.zMoveClamp = 1.76
geo.initialRotation = [-90, 140, 0]
# scale model down from earth dimensions to 0-1
geo.model.setScale(0.1**7, 0.1**7, 0.1**7)
geo.reset()

handler = DAEventHandler()
handler.initialCamPosition = [0, 0, 2.4]

handler.yRotSensitivity /= 4
handler.xMoveSensitivity /= 40
handler.yMoveSensitivity /= 40
handler.zMoveSensitivity /= 4

handler.spaceNavMoveSensitivity /= 5
handler.spaceNavRotSensitivity /= 8

handler.allowXRot = False
handler.allowZRot = False
handler.allowXMove = False

handler.addGeo(geo)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
