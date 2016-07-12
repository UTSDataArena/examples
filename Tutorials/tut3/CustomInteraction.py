# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import getDefaultCamera, getEvent, querySceneRay, SceneNode
from cyclops import *
# from omegaToolkit import ui

from pipelines.objects import BaseObject
# from pipelines.handler import GeometryHandler
from pipelines.eventadapters import MyControllerAdapter
import json

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
        self.model.getMaterial().setColor(Color(0.2,0.2,0.2,1.0), Color(0.0, 0.0,0.0, 0.0))

        self.setSelectableParts()

    def getEyeAndFocusPosition(self):
        """returns a SceneNode containing transform of the camera and of a focus point"""
        cam =  self.model.getPiece("Root/Camera")
        assert cam != None
        focus = cam.getPiece("CameraFocus")
        assert focus != None
        return cam.getPosition(), cam.convertLocalToWorldPosition( focus.getPosition() )

    def setSelectableParts(self):    
        self.selectableNodes = []
        self.model.setSelectable(False)
        for pieceName in self.model.listPieces("Root"):
            if pieceName == "Camera": #dont extract the camera yet
                continue
            mod = self.model.getPiece("Root/" + pieceName)
            if pieceName.startswith("cb"):
                if mod != None:
                    mod.setSelectable(True)
                    self.selectableNodes.append(mod)

            else:
                mod.setSelectable(False)

    def getSelectableNodes(self):
        return self.selectableNodes


class CameraHandler:
    def __init__(self):
        self.camManipController = ManipulatorController.create()
        self.manipulator = TerrainManipulator.create()
        self.camManipController.setManipulator(self.manipulator)
        
        self.eventAdapter = MyControllerAdapter(self.manipulator)
        #self.camManipController.setEventAdapter(self.eventAdapter)

    def setNode(self, node):
        self.manipulator.setTerrainNode(node)
        # self.defaultColor = self.node.getColor()

    def setCameraHome(self, eye, center):
        self.manipulator.setHome(eye, center, Vector3(0,0,1))

    def home(self):
        self.manipulator.home()

    def onEvent(self):
        """Callback for omegalib to register with `setEventFunction`."""
        e = getEvent()
        self.camManipController.onEvent(e)


    def onUpdate(self, frame, time, dt):
        if self.eventAdapter != None:
            self.eventAdapter.onUpdate(self.camManipController)


class SceneHandler:
    def __init__(self, modelController):
        self.modelController = modelController

        self.ui = UiModule.createAndInitialize()
        self.wf = self.ui.getWidgetFactory()
        self.uiroot = self.ui.getUi()

        containerSize = Vector2(300, 100)
        self.container = self.wf.createContainer('container', self.uiroot, ContainerLayout.LayoutVertical)
        self.container.setAutosize(False)
        self.container.setSize(containerSize)
        self.container.setVisible(False)

        self.container2 = self.wf.createContainer('container', self.uiroot, ContainerLayout.LayoutFree)
        self.container2.setStyle('fill: black; border: 0 black; alpha: 0.6;')
        self.container2.setAutosize(False)
        self.container2.setSize(containerSize)
        self.container2.setVisible(False)

        self.container.setLayer(WidgetLayer.Front)
        self.label = self.makeLabel("label1")
        self.label2 = self.makeLabel("label2")

        self.lastMousePos = None


        with open('buildinginfo.json') as data_file:    
            self.buildinginfo = json.load(data_file)


    def colorHovered(self, node, dist):
        if node != None:
            # print node.getName(), dist
            for n in self.modelController.getSelectableNodes():
                if n.getName() == node.getName():
                    n.getMaterial().setColor(Color(1.0,1.0,1.0,1.0), Color(0.2, 0.2,0.2, 0.2))
                else:
                    n.getMaterial().setColor(Color(0.2,0.2,0.2,1.0), Color(0.0, 0.0,0.0, 0.0))
        else:
            for n in self.modelController.getSelectableNodes():
                n.getMaterial().setColor(Color(0.2,0.2,0.2,1.0), Color(0.0, 0.0,0.0, 0.0))

    def makeLabel(self, name):
        label = self.wf.createLabel(name, self.container, '')
        label.setLayer(WidgetLayer.Front)
        label.setAutosize(True)
        label.setStyle('font: fonts/arial.ttf 30; color: white; alpha: 1.0;')
        label.setBlendMode(WidgetBlendMode.BlendNormal)
        label.setStyleValue('align', 'middle-left') 
        return label


        

    def onClicked(self, node, dist):
        if node != None:
            onLeft = 1 if (getDisplayPixelSize()[0] / 2.0 > self.mouseClickPos[0] ) else -1
            pos = self.mouseClickPos + onLeft * Vector3(150, 0, 0)
            self.updateTextInfo(node)
            self.container.setCenter(pos)
            self.container2.setCenter(pos)
            self.container.setVisible(True)
            self.container2.setVisible(True)
        else:
            self.container.setVisible(False)            
            self.container2.setVisible(False)

    def onEvent(self):
        """Callback for omegalib to register with `setEventFunction`."""
        e = getEvent()
        if(e.getServiceType() == ServiceType.Pointer or e.getServiceType() == ServiceType.Wand):
            r = getRayFromEvent(e)

            # Button mappings are different when using wand or mouse
            confirmButton = EventFlags.Button1
            if(e.getServiceType() == ServiceType.Wand): confirmButton = EventFlags.Button5
            
            if(r[0]): 
                # When the confirm button is pressed:
                if(e.isButtonDown(confirmButton)):
                    self.mouseClickPos = e.getPosition()
                    querySceneRay(r[1], r[2], self.onClicked, QueryFlags.QuerySort | QueryFlags.QueryFirst)
                else:
                    querySceneRay(r[1], r[2], self.colorHovered, QueryFlags.QuerySort | QueryFlags.QueryFirst)

    def updateTextInfo(self, selectedNode):
        if self.buildinginfo["buildings"].has_key(selectedNode.getName()):
            building = self.buildinginfo["buildings"][selectedNode.getName()]
            self.label.setText("Building: " + selectedNode.getName())
            self.label2.setText("Height: " +  str(building["height"]) + "m")
        else:
            self.label.setText("Building: N.A")
            self.label2.setText("Height: N.A")


# handler = GeometryHandler()
modelController = UTSModelController()
camPosition, focusPosition = modelController.getEyeAndFocusPosition()

camManipulator = CameraHandler()
#set Camera starting position to the home camera
camManipulator.setCameraHome(camPosition, focusPosition)
camManipulator.setNode(modelController.model)

sceneHandler = SceneHandler(modelController)






setEventFunction(sceneHandler.onEvent)
setEventFunction(camManipulator.onEvent)

setUpdateFunction(camManipulator.onUpdate)

