# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import setEventFunction, setUpdateFunction
from GeoLoader.GeometryFile import OTL
from GeoLoader.DAEventHandler import OTLHandler

examples = [
        ("/local/examples/barchart/barchart.hdanc", "Object/barchart", "barchart1"),
]

geo = OTL(examples[0])
handler = OTLHandler()
handler.initialCamPosition = [0, -3, 4]

handler.allowXRot = False
handler.allowZRot = False
handler.allowYMove = False

handler.addGeo(geo)
setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
