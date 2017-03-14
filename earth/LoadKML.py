# TODO: append GeoLoader package to python search path in omegalib: workaround
import os.path, sys
basePath = os.path.dirname(os.path.abspath(__file__)) # for current dir of file
modulePath = os.path.dirname(basePath) # for GeoLoader packages - '/local/examples'
sys.path.append(modulePath) 

from omega import setEventFunction, setUpdateFunction
from pipelines.objects import KML 
from pipelines.handler import GeometryHandler

modelFile = basePath + "/mapquest_osm.earth"
geo = KML(modelFile)
geo.addKml(basePath + "/polygon.kml")
# Polygon and Path working, Placemark Points, GroundOverlays not (no HTML)
# Polygon needs to be elevated
# TODO KMZ

geo.yRotClamp = 360
geo.xRotClamp = geo.zRotClamp = 0
geo.xMoveClamp = geo.yMoveClamp = geo.zMoveClamp = 0.07
geo.initialRotation = [-90, 122, 0]
# scale model down from earth dimensions to 0-1
geo.model.setScale(0.1**7, 0.1**7, 0.1**7)
geo.reset()

handler = GeometryHandler()
handler.initialCamPosition = [0, -0.36, 0.6]

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
