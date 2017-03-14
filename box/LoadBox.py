# TODO: append GeoLoader package to python search path in omegalib: workaround
import os.path, sys
basePath = os.path.dirname(os.path.abspath(__file__)) # for current dir of file
modulePath = os.path.dirname(basePath) # for GeoLoader packages - '/local/examples'
sys.path.append(modulePath) 

from pipelines.objects import Geometry
from pipelines.handler import GeometryHandler 

fileToLoad = basePath + "/box.obj"

geo = Geometry(fileToLoad)

handler = GeometryHandler()
handler.addGeo(geo)
handler.initialCamPosition = [1, 0, 5]

geo2 = Geometry(fileToLoad)
geo2.initialPosition = [2,0,0]
handler.addGeo(geo2)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
