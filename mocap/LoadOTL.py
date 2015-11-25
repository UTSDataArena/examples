# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/home/fabian/Code/examples')

from omega import setEventFunction, setUpdateFunction
from GeoLoader.GeometryFile import OTL
from GeoLoader.DAEventHandler import OTLHandler

examples = [
        ("/home/fabian/Code/examples/mocap/otl/mocap.hdanc", "Object/mocap", "mocap1"),
]

geo = OTL(examples[0])

handler = OTLHandler()
handler.initialCamPosition = [0, 0, 40]

handler.addGeo(geo)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
