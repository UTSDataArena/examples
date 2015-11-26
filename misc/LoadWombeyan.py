# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import setEventFunction, setUpdateFunction
from cyclops import ProgramAsset, PrimitiveType, UniformType
from GeoLoader.GeometryFile import GeometryFile
from GeoLoader.DAEventHandler import DAEventHandler

shaderPath = "/da/sw/omegalib/darren.omegalib/core/modules/pointCloud/shaders"
program = ProgramAsset()
program.name = "pointsDepth"
program.vertexShaderName = shaderPath + "/Sphere.vert"
program.fragmentShaderName = shaderPath + "/Sphere.frag"
program.geometryShaderName = shaderPath + "/Sphere.geom"
program.geometryOutVertices = 4
program.geometryInput = PrimitiveType.Points
program.geometryOutput = PrimitiveType.TriangleStrip

filename = "/da/proj/caves/Victoria_Arch/wcr03_victoria_arch_3cm_shape_rotYup_binary.ply"
cave = GeometryFile(filename)
cave.setShader(program)
cave.getMaterial().addUniform('pointScale', UniformType.Float)
cave.getMaterial().getUniform('pointScale').setFloat(0.01)

cave.xMoveClamp = cave.yMoveClamp = cave.zMoveClamp = 50

handler = DAEventHandler()
handler.cameraControl = True

handler.allowZRot = False
handler.xMoveSensitivity *= 4
handler.yMoveSensitivity *= 4
handler.zMoveSensitivity *= 4
handler.xRotSensitivity *= 7
handler.yRotSensitivity *= 7
handler.zRotSensitivity *= 7

handler.initialCamPosition = [-22, -11, -7]
handler.initialCamRotation = [0, 180, 0]

handler.addGeo(cave)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
