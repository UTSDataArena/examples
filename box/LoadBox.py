# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from pipelines.objects import Geometry
from pipelines.handler import GeometryHandler 

fileToLoad = "/local/examples/box/box.obj"

geo = Geometry(fileToLoad)

handler = GeometryHandler()
handler.addGeo(geo)
handler.initialCamPosition = [1, 0, 5]

geo2 = Geometry(fileToLoad)
geo2.initialPosition = [2,0,0]
handler.addGeo(geo2)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)