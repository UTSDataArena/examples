from cyclops import *
from omega import *
from daHEngine import LoaderTools

LoaderTools.registerDAPlyLoader() 


scene = getSceneManager()
scene.setBackgroundColor(Color(0.1,0.1,0.1,1))

fileToLoad = "mtcars.ply"

def addModel(fileToLoad, faceScreen=False):
	# Load a static model
	mdlModel = ModelInfo()
	mdlModel.name = fileToLoad
	mdlModel.path = fileToLoad
	mdlModel.optimize=False # optimising takes a LONG time..
	if faceScreen:
		mdlModel.readerWriterOptions = "shiftVerts faceScreen" 
	return mdlModel

# Let the tetrahdeons face the screen for demo purposes
scene.loadModel(addModel(fileToLoad,faceScreen=True))
model = StaticObject.create(fileToLoad)
model.setName(fileToLoad)
model.getMaterial().setAdditive(True)

scene.loadModel(addModel("axes.ply"))
axes = StaticObject.create("axes.ply")
axes.setName("axes.ply")
model.addChild(axes)


#create a camera controller
camManipController = ManipulatorController.create()
#set its manipulator
manipulator = NodeTrackerManipulator.create()
camManipController.setManipulator(manipulator, None)
#set the node to track
manipulator.setTrackedNode(model)

#pass down events
def onEvent():
    e = getEvent()
    camManipController.onEvent(e)
    
setEventFunction(onEvent)
