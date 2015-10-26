from euclid import Vector3
from omega import SceneNode, Space, quaternionFromEulerDeg
from cyclops import ModelInfo, StaticObject, getSceneManager

class GeometryFile():
	_sceneNodeCount = 0

        # TODO: fix this
        # numbers temporarily hard coded, getBoundCenter doesn't seem to work
        _offsets = {
                "/da/mannequinShoot/exports/TammyLuk/TammyLuk_look1_initial.fbx": Vector3(-0.99, -0.02, -0.62),
        }

	def makeBase(self):
		GeometryFile._sceneNodeCount += 1
		self.base = SceneNode.create("Geometry_" + str(GeometryFile._sceneNodeCount))
		self.initialRot = self.base.getOrientation()
		self.initialAngles = list(self.base.getOrientation().get_euler())
		self.initialPosition = list(self.base.getPosition())

                self.reset()

        def __init__(self): 
                self.base = None

		self.angles = None
		self.position = None

		self.initialRot = None
		self.initialAngles = None
                self.initialPosition = None

		self.xAngClamp = 90
		self.yAngClamp = 90
		self.zAngClamp = 90

                self.xPosClamp = 1
                self.yPosClamp = 1
                self.zPosClamp = 1

		self.modelInfos = []

		self.makeBase()

        def reset(self):
                self.angles = self.initialAngles
                self.position = self.initialPosition

	def addModel(self, fileToLoad):
		# Load a static model
		mdlModel = ModelInfo()
		mdlModel.name = fileToLoad
		mdlModel.path = fileToLoad
		mdlModel.size = 1.0
                # optimising takes a LONG time..
		mdlModel.optimize = False 
		self.modelInfos.append(mdlModel)
		return self.modelInfos[-1]

	def loadModel(self, fileToLoad, textured=True):
		getSceneManager().loadModel(self.addModel(fileToLoad))
		newModel = StaticObject.create(fileToLoad)
		newModel.setName(fileToLoad)
		self.setModel(newModel, textured)

	def setModel(self, model, textured=True):
		if textured:
			model.setEffect("textured")
			model.setEffect("@unlit")
		else:
			model.setEffect("colored -d white -C")

		model.getMaterial().setDoubleFace(True)

                # translate model if getBoundCenter would work
		if model.getName() not in GeometryFile._offsets.keys():
			GeometryFile._offsets[model.getName()] = -model.getBoundCenter()
		model.initialPosition = GeometryFile._offsets[model.getName()]

		self.base.addChild(model)

	def deleteModels(self):
		while self.base.numChildren() > 0:
			self.base.removeChildByIndex(0)

        def updateModel(self, newAngles, newPosition):
            self.angles = [
                    min(max(self.angles[0] + newAngles[0], -self.xAngClamp), self.xAngClamp),
                    min(max(self.angles[1] + newAngles[1], -self.yAngClamp), self.yAngClamp),
                    min(max(self.angles[2] + newAngles[2], -self.zAngClamp), self.zAngClamp)
            ]

            self.base.setOrientation(self.initialRot * quaternionFromEulerDeg(*self.angles))

            self.position = [
                    min(max(self.position[0] + newPosition[0], -self.xPosClamp), self.xPosClamp),
                    min(max(self.position[1] + newPosition[1], -self.yPosClamp), self.yPosClamp),
                    min(max(self.position[2] + newPosition[2], -self.zPosClamp), self.zPosClamp)
            ]

            self.base.setPosition(Vector3(*self.position))
            self.base.translate(Vector3(*self.position), Space.Local)
