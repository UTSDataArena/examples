# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import setEventFunction, setUpdateFunction
from pipelines.objects import Geometry
from pipelines.handler import GeometryHandler

fileToLoad = "/local/examples/fashion/Mook_mix1_initial.fbx"

model = Geometry(fileToLoad)
# original model is too big
model.model.setScale(0.1, 0.1, 0.1)
model.zMoveClamp = 33

handler = GeometryHandler()
handler.initialCamPosition = [0, 0, 35]

handler.addGeo(model)
handler.allowXRot = False
handler.allowZRot = False
handler.zMoveSensitivity *= 10

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
