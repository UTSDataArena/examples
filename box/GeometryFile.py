from euclid import Vector3
from omega import SceneNode, Space, quaternionFromEulerDeg
from cyclops import ModelInfo, StaticObject, getSceneManager

class GeometryFile():
        """The class provides a wrapper to load a geometry file into omegalib.

        An instantiated object is registered at a `DAEventHandler` object and encapsulates the geometry.
        """
	_sceneNodeCount = 0

        #: TODO fix this
        # numbers temporarily hard coded, getBoundCenter doesn't seem to work
        _offsets = {
                "/da/mannequinShoot/exports/TammyLuk/TammyLuk_look1_initial.fbx": Vector3(-0.99, -0.02, -0.62),
        }

	def makeBase(self):
                """This is an internal method."""

		GeometryFile._sceneNodeCount += 1
		self.base = SceneNode.create("Geometry_" + str(GeometryFile._sceneNodeCount))
		self.initialAngles = self.base.getOrientation()
		self.initialPosition = list(self.base.getPosition())

                self.reset()

        def __init__(self, fileToLoad): 
                """The constructor provides some parameters to tune the object interaction.
                
                :param fileToLoad: Path to the geo file
                :type fileToLoad: String

                :return: instantiated object
                :rtype: GeometryFile object
                """

                self.base = None

		self.angles = None
		self.position = None

		self.initialAngles = None
                self.initialPosition = None

                #: Set maximum rotation here.
		self.xAngClamp = 90
		self.yAngClamp = 90
		self.zAngClamp = 90

                #: Set maximum translation here.
                self.xPosClamp = 1
                self.yPosClamp = 1
                self.zPosClamp = 1

                self.textured = True

		self.modelInfos = []

		self.makeBase()
                self.loadModel(fileToLoad)

        def reset(self):
                """Reset to original position"""
                self.angles = list(self.initialAngles.get_euler())
                self.position = self.initialPosition

	def loadModel(self, fileToLoad):
                """Loads a geometry model from the given file.

                :param fileToLoad: Path to geo file
                """
		modelInfo = ModelInfo()
		modelInfo.name = fileToLoad
		modelInfo.path = fileToLoad
		modelInfo.size = 1.0
                # optimising takes a LONG time..
		modelInfo.optimize = False 
		self.modelInfos.append(modelInfo)

		getSceneManager().loadModel(modelInfo)
		newModel = StaticObject.create(fileToLoad)
		newModel.setName(fileToLoad)

		if self.textured:
			newModel.setEffect("textured")
			newModel.setEffect("@unlit")
		else:
			newModel.setEffect("colored -d white -C")

		newModel.getMaterial().setDoubleFace(True)

                # translate newModel if getBoundCenter would work
		if newModel.getName() not in GeometryFile._offsets.keys():
			GeometryFile._offsets[newModel.getName()] = -newModel.getBoundCenter()
		newModel.initialPosition = GeometryFile._offsets[newModel.getName()]

		self.base.addChild(newModel)

	def deleteModels(self):
		while self.base.numChildren() > 0:
			self.base.removeChildByIndex(0)

        def updateModel(self, newAngles, newPosition):
                """Callback for DAEventhandler to update coordinates.

                :param newAngle: Rotation vector
                :param newPosition: Translation vector
                :type newAngle: List with 3 double values
                :type newPosition: List with 3 double values

                This method is used to change the angle and position or the object with the given vectors
                """
                self.angles = [
                        min(max(self.angles[0] + newAngles[0], -self.xAngClamp), self.xAngClamp),
                        min(max(self.angles[1] + newAngles[1], -self.yAngClamp), self.yAngClamp),
                        min(max(self.angles[2] + newAngles[2], -self.zAngClamp), self.zAngClamp)
                ]

                self.base.setOrientation(self.initialAngles * quaternionFromEulerDeg(*self.angles))

                self.position = [
                        min(max(self.position[0] + newPosition[0], -self.xPosClamp), self.xPosClamp),
                        min(max(self.position[1] + newPosition[1], -self.yPosClamp), self.yPosClamp),
                        min(max(self.position[2] + newPosition[2], -self.zPosClamp), self.zPosClamp)
                ]

                # update position to have newest pivot for rotation
                self.base.setPosition(Vector3(*self.position))
                self.base.translate(Vector3(*self.position), Space.Local)
