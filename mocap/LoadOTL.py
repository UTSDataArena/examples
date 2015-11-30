# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import setEventFunction, setUpdateFunction
from pipelines.objects import OTL
from pipelines.handler import OTLHandler

examples = [
        ("/local/examples/mocap/otl/mocap.hdanc", "Object/mocap", "mocap1"),
]

geo = OTL(examples[0])

handler = OTLHandler()
handler.initialCamPosition = [0, 0, 40]

handler.addGeo(geo)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
