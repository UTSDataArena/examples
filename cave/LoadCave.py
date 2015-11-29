# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import setEventFunction, setUpdateFunction
from cyclops import ProgramAsset, PrimitiveType, UniformType
from GeoLoader.GeometryFile import GeometryFile
from GeoLoader.DAEventHandler import DAEventHandler

shaderPath = "/local/omegalib/modules/pointCloud/shaders"
program = ProgramAsset()
program.name = "pointsDepth"
program.vertexShaderName = shaderPath + "/Sphere.vert"
program.fragmentShaderName = shaderPath + "/Sphere.frag"
program.geometryShaderName = shaderPath + "/Sphere.geom"
program.geometryOutVertices = 4
program.geometryInput = PrimitiveType.Points
program.geometryOutput = PrimitiveType.TriangleStrip

cave = GeometryFile("/local/examples/cave/wcc04_archentrance_9pct.ply")
cave.initialRotation = [-90, 150, 0]
cave.initialPosition = [2, 6, -18]
cave.setShader(program)
cave.getMaterial().addUniform('pointScale', UniformType.Float)
cave.getMaterial().getUniform('pointScale').setFloat(0.07)

cave.xMoveClamp = cave.yMoveClamp = cave.zMoveClamp = 20

handler = DAEventHandler()
handler.toggleView()

handler.allowZRot = False
handler.xMoveSensitivity *= 4
handler.yMoveSensitivity *= 4
handler.zMoveSensitivity *= 4
handler.xRotSensitivity *= 8
handler.yRotSensitivity *= 8
handler.zRotSensitivity *= 8

handler.spaceNavRotSensitivity *= 7

handler.addGeo(cave)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
