# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import getDefaultCamera, getEvent, querySceneRay, SceneNode
from cyclops import *

from pipelines.objects import BaseObject
# from pipelines.handler import GeometryHandler
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
        self.model.setSelectable(True)

        self.setSelectableParts()

    def getEyeAndFocusPosition(self):
        """returns a SceneNode containing transform of the camera and of a focus point"""
        cam =  self.model.getPiece("Root/Camera")
        assert cam != None
        focus = cam.getPiece("CameraFocus")
        assert focus != None
        return cam.getPosition(), cam.convertLocalToWorldPosition( focus.getPosition() )

    def setSelectableParts(self):    
        self.model.setSelectable(False)
        for pieceName in self.model.listPieces("Root"):
            if pieceName == "Camera": #dont extract the camera yet
                return
            mod = self.model.getPiece("Root/" + pieceName)
            if pieceName.startswith("cb"):
                if mod != None:
                    mod.setSelectable(True)
                    print pieceName, mod.getName()
            else:
                mod.setSelectable(False)

def printnode(node, dist):
    if node != None:
        print node.getName(), dist


class CameraHandler:
    def __init__(self):
        self.camManipController = ManipulatorController.create()
        self.manipulator = TerrainManipulator.create()
        self.camManipController.setManipulator(self.manipulator)
        
        self.eventAdapter = MyControllerAdapter(self.manipulator)
        #self.camManipController.setEventAdapter(self.eventAdapter)

    def setTerrainNode(self, node):
        self.manipulator.setTerrainNode(node)

    def setCameraHome(self, eye, center):
        self.manipulator.setHome(eye, center, Vector3(0,0,1))

    def home(self):
        self.manipulator.home()

    def onEvent(self):
        """Callback for omegalib to register with `setEventFunction`."""
        e = getEvent()
        self.camManipController.onEvent(e)

        if(e.getServiceType() == ServiceType.Pointer or e.getServiceType() == ServiceType.Wand):
            r = getRayFromEvent(e)

            # Button mappings are different when using wand or mouse
            confirmButton = EventFlags.Button1
            if(e.getServiceType() == ServiceType.Wand): confirmButton = EventFlags.Button5
            
            # When the confirm button is pressed:
            if(e.isButtonDown(confirmButton) or e.isFlagSet(EventFlags.Left)):
                if(r[0]): 
                    querySceneRay(r[1], r[2], printnode, QueryFlags.QuerySort | QueryFlags.QueryFirst)


    def onUpdate(self, frame, time, dt):
        if self.eventAdapter != None:
            self.eventAdapter.onUpdate(self.camManipController)


# handler = GeometryHandler()
controller = UTSModelController()
camPosition, focusPosition = controller.getEyeAndFocusPosition()

camManipulator = CameraHandler()
#set Camera starting position to the home camera
camManipulator.setCameraHome(camPosition, focusPosition)
camManipulator.setTerrainNode(controller.model)



setEventFunction(camManipulator.onEvent)
setUpdateFunction(camManipulator.onUpdate)

