# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import setEventFunction, setUpdateFunction
from GeoLoader.GeometryFile import GeometryFile
from GeoLoader.DAEventHandler import DAEventHandler

brainFile = "/da/proj/paulBourke/brain/model.obj"

brain = GeometryFile(brainFile)
brain.initialRotation = [-80, 100, 10]
brain.initialPosition = [0, 0.03, -0.9]
brain.reset()

handler = DAEventHandler()

handler.allowXMove = handler.allowYMove = handler.allowZMove = False

handler.addGeo(brain)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
