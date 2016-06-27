# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import getDefaultCamera, getEvent, ServiceType, EventFlags, EventType, isStereoEnabled, toggleStereo, quaternionFromEulerDeg, SceneNode, Space
from cyclops import *

from pipelines.objects import BaseObject
from pipelines.handler import GeometryHandler

fileToLoad = "/local/examples/Tutorials/tut3/uts.osgt"



class UTSModelController(BaseObject):

	def __init__(self):
		BaseObject.__init__(self)


		# Load a static model
		modelInfo = ModelInfo()
		modelInfo.name = "UTS"
		modelInfo.path = fileToLoad
		modelInfo.size = 65.0
		modelInfo.optimize = False
		getSceneManager().loadModel(modelInfo)

		self.model = StaticObject.create("UTS")

	def updateModel(self, newRotation, newPosition):
		self.model.rotate(Vector3(1, 0, 0), newRotation[0], Space.World)
		self.model.rotate(Vector3(0, 1, 0), newRotation[1], Space.World)
		self.model.rotate(Vector3(0, 0, 1), newRotation[2], Space.World)


	def getModelCameraMatrix(self):
		"""returns a SceneNode containing the matrix transform of the camera"""
		camMat =  self.model.getPiece("Root/Camera")
		assert camMat != None
		return camMat

class CustomEventHandler():
	def __init__(self):
		pass

	def onEvent(self):
        """Callback for omegalib to register with `setEventFunction`."""
        pass

    def onUpdate(self, frame, time, dt):
        """Callback for omegalib to register with `setUpdateFunction`."""
        pass

# handler = GeometryHandler()
controller = UTSModelController()

# set the scene camera to the transform of the scene-camera in blender
camMat = controller.getModelCameraMatrix()
getDefaultCamera().setPosition(camMat.getPosition())
getDefaultCamera().setOrientation(camMat.getOrientation())
# handler.addObject(controller)

# getDefaultCamera().
# setEventFunction(handler.onEvent)
# setUpdateFunction(handler.onUpdate)
