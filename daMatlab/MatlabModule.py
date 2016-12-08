from cyclops import *
from daMatlab import *

mm = MatlabModule.createAndInitialize()

scene = mm.getSceneManager()

program = ProgramAsset()
program.name = "MatlabModule"
scene.addProgram(program)

getDefaultCamera().setBackgroundColor(Color(1,1,1,1))

# Update function
def onUpdate(frame, t, dt):
    
    mm.addNewGeometry()

# register the update function
setUpdateFunction(onUpdate)
