# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import setEventFunction, setUpdateFunction
from pipelines.objects import Geometry
from pipelines.handler import GeometryHandler

brain = Geometry("/da/proj/paulBourke/brain/model.obj")
brain.initialRotation = [-80, 100, 10]
brain.initialPosition = [0, 1, -28]
brain.model.setScale(0.1, 0.1, 0.1)
brain.reset()

handler = GeometryHandler()

handler.allowXMove = handler.allowYMove = handler.allowZMove = False

handler.addGeo(brain)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
