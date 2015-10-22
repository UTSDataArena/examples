from omega import *
from cyclops import *

scene = getSceneManager()

# Load a static model
torusModel = ModelInfo()
torusModel.name = "torus"
torusModel.path = "/local/omegalib/modules/cyclops/examples/helloEarth/mapquest_osm.earth"
torusModel.optimize = False
scene.loadModel(torusModel)

# Create a scene object using the loaded model
torus = StaticObject.create("torus")
#torus.setEffect("colored")
setNearFarZ(1, 4 * torus.getBoundRadius())

cam = getDefaultCamera()

#cam.setPosition(torus.getBoundCenter())
cam.getController().setSpeed(3000000)
