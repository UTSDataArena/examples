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

    def getEyeAndFocusPosition(self):
        """returns a SceneNode containing transform of the camera and of a focus point"""
        cam =  self.model.getPiece("Root/Camera")
        focus = cam.getPiece("CameraFocus")
        assert focus != None
        assert cam != None
        return cam.getPosition(), cam.convertLocalToWorldPosition( focus.getPosition() )

class MyWandAdapter(EventAdapter):
    def __init__(self):
        EventAdapter.__init__(self)

    def preMapping(self):
        pass

    def mapButton(self):
        e = self.getLastEvent()
        if e.getServiceType() == ServiceType.Wand:
            if(e.isButtonDown( EventFlags.Button6 )): # Analog
                return OsgMouseButtons.LEFT_MOUSE_BUTTON # emulate a drag, rotate event

        # print event.getType()
        return 19

    def mapXY(self):
        e = self.getLastEvent()
        analogUD = e.getAxis(1)

        return Vector2(1,2)

    def setInputRange(self):
        e = self.getLastEvent()
        return (0,0,100,100)

    def mapScrollingMotion(self):
        e = self.getLastEvent()
        # L1 button
        if e.isButtonDown( EventFlags.Button5 ) :
            return OsgScrollingMotion.SCROLL_DOWN
        elif e.isButtonDown( EventFlags.Button7 ) :
            return OsgScrollingMotion.SCROLL_UP
        else:
            return OsgScrollingMotion.SCROLL_NONE

    def mapEventType(self):
        e = self.getLastEvent()
        return OsgEventType.MOVE

    def postMapping(self):
        pass



class MyControllerAdapter(EventAdapter):
    def __init__(self, manipulator):
        EventAdapter.__init__(self)
        print "using a controller event adapter"
        self.isRotating = False
        self.isPanning = False
        self.isZooming = False
        self.sendEvent = OsgEventType.NONE
        self.simulatedXPos = 0
        self.simulatedYPos = 0
        self.leftAnalogFactor = 0.01
        self.rightAnalogFactor = 0.01
        self.zoomAnalogFactor = 0.01
        self.started = False
        self.manipulator = manipulator


    def getOsgEvent(self, hasMoved, previousState):
        if hasMoved:
            if not previousState: #starting into new state
                sendEvent = OsgEventType.PUSH
            else:
                sendEvent = OsgEventType.DRAG
            return sendEvent
        elif previousState: #if analog stick has just been reset to start position
            sendEvent = OsgEventType.RELEASE 
            return sendEvent
        else:
            return self.sendEvent #don't change sendEvent


    def preMapping(self):
        self.started = True
        e = self.getLastEvent()
        if e.getServiceType() != ServiceType.Controller:
            return

        if e.getType() != EventType.Update:
            return
            
        leftAnalogLR = e.getAxis(0)
        leftAnalogUD = e.getAxis(1)
        leftStickMoved = (abs(leftAnalogUD) + abs(leftAnalogLR)) > 0.001
        self.sendEvent = self.getOsgEvent(leftStickMoved, self.isRotating)
        self.isRotating = leftStickMoved

        rightAnalogLR = e.getAxis(2)
        rightAnalogUD = e.getAxis(3)
        rightStickMoved = abs(rightAnalogUD) + abs(rightAnalogLR) > 0.001
        self.sendEvent = self.getOsgEvent(rightStickMoved, self.isPanning)
        self.isPanning = rightStickMoved


        L2press = e.getAxis(4)
        L3press = e.getAxis(5)
        zoomPressed = abs(L2press) + abs(L3press) > 0.05
        self.sendEvent = self.getOsgEvent(zoomPressed, self.isZooming)
        self.isZooming = zoomPressed



    def mapButton(self):
        if self.isRotating:
            return OsgMouseButtons.LEFT_MOUSE_BUTTON # emulate a drag/rotate event
        elif self.isPanning:
            return OsgMouseButtons.MIDDLE_MOUSE_BUTTON
        elif self.isZooming:
            return OsgMouseButtons.RIGHT_MOUSE_BUTTON
        else:
            return 0


    def mapXY(self):
        e = self.getLastEvent()
        if e.getServiceType() != ServiceType.Controller:
            return Vector2(0,0)

        if self.isRotating or self.isPanning:
            if self.isRotating:
                i,j = (0,1)
                factor = self.leftAnalogFactor
            else:
                i,j = (2,3)
                factor = self.rightAnalogFactor

            analogLR = -e.getAxis(i) * factor
            analogUD = -e.getAxis(j) * factor

            self.simulatedXPos += analogLR 
            self.simulatedYPos += analogUD 
        
        elif self.isZooming:
            self.simulatedXPos = 0
            self.simulatedYPos += (e.getAxis(4) - e.getAxis(5)) * self.zoomAnalogFactor

        else:
            self.simulatedXPos = 0
            self.simulatedYPos = 0


        return Vector2(self.simulatedXPos, self.simulatedYPos)

    def setInputRange(self):
        return (-1.0,-1.0,1.0,1.0)

    def mapScrollingMotion(self):
        return OsgScrollingMotion.SCROLL_NONE

    def mapEventType(self):
        return self.sendEvent

    def mapKeySymbol(self):
        e = self.getLastEvent()
        if e.getType() == EventType.Down:
            if e.isButtonDown(EventFlags.Button4): #triangle on ps4
                self.manipulator._home(0.0) #directly set home
                return OsgKeySymbol.KEY_Space
        return OsgKeySymbol.KEY_F35 #aka void

    def postMapping(self):
        pass

    def isMoving(self):
        return self.started and  \
                (self.isRotating or self.isPanning or self.isZooming) and \
                self.sendEvent == OsgEventType.DRAG

    def onUpdate(self, camManipController):
        if isMoving():
            # workaround for smooth rotations, as omicron does not fire an event
            # if the joystick is kept in the same position
            camManipController.onEvent(getLastEvent())


class ControllerCameraManipulator:
    def __init__(self):
        self.camManipController = CameraManipulator.create()
        self.manipulator = TerrainManipulator.create()
        self.camManipController.setManipulator(self.manipulator)
        
        self.eventAdapter = MyControllerAdapter(self.manipulator)
        self.camManipController.setEventAdapter(self.eventAdapter)

    def setTrackedNode(self, node):
        self.manipulator.setTrackedNode(node)

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

setEventFunction(camManipulator.onEvent)
setUpdateFunction(camManipulator.onUpdate)