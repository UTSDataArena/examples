# TODO: append GeoLoader package to python search path in omegalib: workaround
import os.path, sys
basePath = os.path.dirname(os.path.abspath(__file__)) # for current dir of file
modulePath = os.path.dirname(basePath) # for GeoLoader packages - '/local/examples'
sys.path.append(modulePath) 

from omega import setEventFunction, setUpdateFunction
from pipelines.objects import Geometry
from pipelines.handler import GeometryHandler

fileToLoad = basePath + "/Mook_mix1_initial.fbx"

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
