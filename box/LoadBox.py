# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import setEventFunction, setUpdateFunction
from GeoLoader.GeometryFile import GeometryFile
from GeoLoader.DAEventHandler import DAEventHandler

fileToLoad = "/local/examples/box/box.obj"
fileToLoad2 = "/local/examples/box/box_translated.obj"

geo = GeometryFile(fileToLoad)
geo2 = GeometryFile(fileToLoad2)
geo2.initialPosition = [1, 0, 0]
geo2.reset()

handler = DAEventHandler()
handler.initialCamPosition = [0, 0, 3]
handler.resetCamera()

handler.addGeo(geo)
handler.addGeo(geo2)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
