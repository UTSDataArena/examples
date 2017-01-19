

# TODO: append GeoLoader package to python search path in omegalib: workaround
import os.path, sys
basePath = os.path.dirname(os.path.abspath(__file__)) # for current dir of file
modulePath = os.path.dirname(basePath) # for GeoLoader packages - '/local/examples'
sys.path.append(modulePath) 

from omega import setEventFunction, setUpdateFunction
from cyclops import ProgramAsset, PrimitiveType, UniformType, getSceneManager
from pipelines.objects import Geometry
from pipelines.handler import GeometryHandler
from pipelines.util import vmCheck
from pointCloud import PointCloud

VM = vmCheck()


program = ProgramAsset()
program.name = "pointsDepth"

modelName = "cave"
modelPath = basePath + "/wcc04_archentrance_9pct"
modelExtension = "ply"

shaderPath = "pointCloud/shaders"


if VM:
	pointSize = 8.0
	pointCloudMaker = PointCloud.createAndInitialize(getSceneManager(), modelName, modelPath, modelExtension, pointSize)
	cave = Geometry()
	cave.setStaticObject(pointCloudMaker.getStaticObject())
	program.vertexShaderName = shaderPath + "/pointsVM.vert"
	program.fragmentShaderName = shaderPath + "/pointsVM.frag"
else:
	cave = Geometry(modelPath+"."+modelExtension)
	program.vertexShaderName = shaderPath + "/Sphere.vert"
	program.fragmentShaderName = shaderPath + "/Sphere.frag"
	program.geometryShaderName = shaderPath + "/Sphere.geom"
	program.geometryOutVertices = 4
	program.geometryInput = PrimitiveType.Points
	program.geometryOutput = PrimitiveType.TriangleStrip


cave.initialRotation = [-90, 150, 0]
cave.initialPosition = [2, 6, -18]
cave.setShader(program)

if not VM:
	cave.getMaterial().addUniform('pointScale', UniformType.Float)
	cave.getMaterial().getUniform('pointScale').setFloat(0.07)

cave.xMoveClamp = cave.yMoveClamp = cave.zMoveClamp = 20

handler = GeometryHandler()
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

