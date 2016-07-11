# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import getDefaultCamera, getEvent, ServiceType, EventFlags, EventType, isStereoEnabled, toggleStereo, quaternionFromEulerDeg, SceneNode, Space
from cyclops import *

from pipelines.objects import BaseObject
from pipelines.handler import GeometryHandler
from pipelines.eventadapters import MyControllerAdapter

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

    def getEyeAndFocusPosition(self):
        """returns a SceneNode containing transform of the camera and of a focus point"""
        cam =  self.model.getPiece("Root/Camera")
        focus = cam.getPiece("CameraFocus")
        assert focus != None
        assert cam != None
        return cam.getPosition(), cam.convertLocalToWorldPosition( focus.getPosition() )


class ControllerCameraManipulator:
    def __init__(self):
        self.camManipController = CameraManipulator.create()
        self.manipulator = TerrainManipulator.create()
        self.camManipController.setManipulator(self.manipulator)
        
        self.eventAdapter = MyControllerAdapter(self.manipulator)
        self.camManipController.setEventAdapter(self.eventAdapter)

    def setTerrainNode(self, node):
        self.manipulator.setTerrainNode(node)

    def setCameraHome(self, eye, center):
        self.manipulator.setHome(eye, center, Vector3(0,0,1))

    def home(self):
        self.manipulator.home()

    def onEvent(self):
        """Callback for omegalib to register with `setEventFunction`."""
        self.camManipController.onEvent(getEvent())

    def onUpdate(self, frame, time, dt):
        if self.eventAdapter != None:
            self.eventAdapter.onUpdate(self.camManipController)


# handler = GeometryHandler()
controller = UTSModelController()
camPosition, focusPosition = controller.getEyeAndFocusPosition()

camManipulator = ControllerCameraManipulator()
#set Camera starting position to the home camera
camManipulator.setCameraHome(camPosition, focusPosition)
camManipulator.setTerrainNode(controller.model)

setEventFunction(camManipulator.onEvent)
setUpdateFunction(camManipulator.onUpdate)