# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/home/fabian/Code/examples')

from omega import getDefaultCamera, setEventFunction, setUpdateFunction
from GeoLoader.GeometryFile import OTL
from GeoLoader.DAEventHandler import OTLHandler

examples = [
        ("/home/fabian/Code/examples/barchart/barchart.hdanc", "Object/barchart", "barchart1"),
]

cam = getDefaultCamera()
cam.setControllerEnabled(False)
cam.setPosition(Vector3(0, -5, 0))
cam.setNearFarZ(0.001, 50)

geo = OTL(examples[0])
handler = OTLHandler()

handler.allowXRot = False
handler.allowZRot = False
handler.allowYMove = False

handler.addGeo(geo)
setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
