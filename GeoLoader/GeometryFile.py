from omega import SceneNode, quaternionFromEulerDeg
from cyclops import ModelInfo, StaticObject, getSceneManager

class GeometryFile():
        """The class provides a wrapper to load a geometry file into omegalib.

        An instantiated object is registered at a `DAEventHandler` object and encapsulates the geometry.
        """

        def __init__(self, fileToLoad): 
                """The constructor provides some parameters to tune the object interaction.
                
                :param fileToLoad: Path to the geo file
                :type fileToLoad: String

                :return: instantiated object
                :rtype: GeometryFile object
                """

                self.model = None

		self.position = None

                #: Changing initial position/rotation requires reset() call.
		self.initialRotation = [0, 0, 0]
		self.initialPosition = [0, 0, 0]

                #: Specifies rotation point of the object, requires reset(). (default: center of bounding box)
                self.pivotPoint = [0, 0, 0]

                #: Set maximum rotation here.
                #: TODO Not working so far
		self.xRotClamp = 90
		self.yRotClamp = 90
		self.zRotClamp = 90

                #: Set maximum translation here.
                self.xMoveClamp = 10
                self.yMoveClamp = 10
                self.zMoveClamp = 10

                self.textured = True

		self.modelInfos = []

                self.loadModel(fileToLoad)

                self.reset()

        def reset(self):
                """Reset to initial position.
                
                Update pivot point and set configured initialRotation/Position, redraw with updateModel().
                """

                self.model.getChildByIndex(0).setPosition(*self.pivotPoint)

                self.position = self.initialPosition
                self.model.setOrientation(quaternionFromEulerDeg(*self.initialRotation))

                self.updateModel([0, 0, 0], [0, 0, 0])

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

                self.pivotPoint = list(-newModel.getBoundCenter())

                #: Use parent object to apply correct rotation on initially translated objects.
                self.model = SceneNode.create("Parent")
                self.model.addChild(newModel)

        def updateModel(self, newRotation, newPosition):
                """Callback for DAEventhandler to update coordinates.

                :param newRotation: Rotation vector
                :param newPosition: Translation vector
                :type newRotation: List with 3 double values
                :type newPosition: List with 3 double values

                This method is used to change the angle and position or the object with the given vectors
                """
                angles = [
                        min(max(newRotation[0], -self.xRotClamp), self.xRotClamp),
                        min(max(newRotation[1], -self.yRotClamp), self.yRotClamp),
                        min(max(newRotation[2], -self.zRotClamp), self.zRotClamp)
                ]

                self.model.setOrientation(quaternionFromEulerDeg(*angles) * self.model.getOrientation())

                self.position = [
                        min(max(self.position[0] + newPosition[0], -self.xMoveClamp), self.xMoveClamp),
                        min(max(self.position[1] + newPosition[1], -self.yMoveClamp), self.yMoveClamp),
                        min(max(self.position[2] + newPosition[2], -self.zMoveClamp), self.zMoveClamp)
                ]

                self.model.setPosition(*self.position)
