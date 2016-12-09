from cyclops import *
from daMatlab import *

ip = 30000
port = "127.0.0.1"

mm = MatlabModule.createAndInitialize()
mm.startDataReader(ip, port)

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
