# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import setEventFunction, setUpdateFunction
from pipelines.objects import Geometry
from pipelines.handler import GeometryHandler 

fileToLoad = "/local/examples/box/box.obj"
fileToLoad2 = "/local/examples/box/box_translated.obj"

geo = Geometry(fileToLoad)
geo2 = Geometry(fileToLoad2)
geo2.initialPosition = [2, 0, 0]
geo2.reset()

handler = GeometryHandler()
handler.initialCamPosition = [1, 0, 5]

handler.addGeo(geo)
handler.addGeo(geo2)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
