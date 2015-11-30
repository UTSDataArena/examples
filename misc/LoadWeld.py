# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import setEventFunction, setUpdateFunction
from pipelines.objects import Geometry
from pipelines.handler import GeometryHandler

weld = Geometry("/da/proj/paulBourke/weld/take1.obj")
weld.initialRotation = [-15, 215, -175]
weld.initialPosition = [0.9, 0, -5]
weld.model.setScale(0.1, 0.1, 0.1)
weld.reset()

handler = GeometryHandler()
handler.toggleView()

handler.allowZRot = False
handler.allowXMove = handler.allowYMove = False

handler.addGeo(weld)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
