#
# DATA ARENA Space Navigator Manipulator
#
# [Darren 5Feb15]
#
# Use this program in the Data Arena to manipulate an object with the Space Navigator
#
# Space Navigator Controls:
# Up/Down, Left/Right, Forward/Backwards - Move object in this direction
# Pitch - rotate like a motorbike handle
# Yaw   - rotate like opening a jar
# Roll  - rotate like a doorknob
# Button 1 - reset position and orientation
#

# Necessary libraries
from cyclops import *
import DA_spaceNav
from omega import *
from daHEngine import LoaderTools
import os.path

LoaderTools.registerDAPlyLoader()

sm = getSceneManager()
sm.setBackgroundColor(Color(0.15,0.15,0.2,0))

# Change these lines for initial control sensitivities
rotSensitivity = 0.4
transSensitivity = 0.1

# Change these lines for initial position and orientation of the object
initPos = Vector3(0, -2, 30)
initRot = quaternionFromEulerDeg(0, 0, 0)
rotOffset = quaternionFromEulerDeg(0,0,0)

# Paths to objects
basePath = os.path.dirname(os.path.abspath(__file__))
fileToLoad = basePath + "/opaque.ply"
isoFile = basePath + "/transparent.ply"
townFile = basePath + "/labels.ply"

def addModel(fileToLoad, isText=False):
	# Load a static model
	mdlModel = ModelInfo()
	mdlModel.name = fileToLoad
	mdlModel.path = fileToLoad
	#mdlModel.size = 1.0
	mdlModel.optimize=False # optimising takes a LONG time..
	
	if isText:
		# setting this option will calculate the center of each geode 
		# and add a matrixtransform to represent the translation
		mdlModel.readerWriterOptions = "shiftVerts faceScreen" 
	
	return mdlModel

sm.loadModel(addModel(fileToLoad))
model = StaticObject.create(fileToLoad)
model.setName(fileToLoad)

# isosurface needs to be transparent
sm.loadModel(addModel(isoFile))
isoModel = StaticObject.create(isoFile)
isoModel.setName(isoFile)
isoModel.getMaterial().setTransparent(True)
isoModel.getMaterial().setAdditive(True)
isoModel.getMaterial().setDepthTestEnabled(False)
model.addChild(isoModel)

# labels don't need to be lit
sm.loadModel(addModel(townFile, isText=True))
townsModel = StaticObject.create(townFile)
townsModel.setName(townFile)
townsModel.getMaterial().setLit(False)
model.addChild(townsModel)

model.translate(-model.getBoundCenter(), Space.Local)

cam = getDefaultCamera()
cam.setNearFarZ(0.001, 1000)
cam.setEyeSeparation(0.007)
cam.rotate(rotOffset, Space.Local)

light = Light.create()
light.setPosition(20,15,10)
light.setAttenuation(1,0,0)

light2 = Light.create()
light2.setPosition(-10,-10,15)
light2.setAttenuation(10,0,0)

# On run
if __name__ == "__main__":
	DA_spaceNav.obj = cam
	DA_spaceNav.rotSensitivity = rotSensitivity
	DA_spaceNav.transSensitivity = transSensitivity
	DA_spaceNav.initPos = initPos
	DA_spaceNav.initRot = initRot
	DA_spaceNav.pivotOffset = Vector3(0,-2,0)
	DA_spaceNav.rotOffset = rotOffset
	setEventFunction(DA_spaceNav.onEvent)
	setUpdateFunction(DA_spaceNav.onUpdate)
	DA_spaceNav.reset()
