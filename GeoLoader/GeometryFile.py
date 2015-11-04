from euclid import Vector3
from omega import SceneNode, Space, quaternionFromEulerDeg
from cyclops import ModelInfo, StaticObject, getSceneManager

class GeometryFile():
        """The class provides a wrapper to load a geometry file into omegalib.

        An instantiated object is registered at a `DAEventHandler` object and encapsulates the geometry.
        """

        #: TODO fix this
        # numbers temporarily hard coded, getBoundCenter doesn't seem to work
        _offsets = {
                "/da/mannequinShoot/exports/TammyLuk/TammyLuk_look1_initial.fbx": Vector3(-0.99, -0.02, -0.62),
        }

        def __init__(self, fileToLoad): 
                """The constructor provides some parameters to tune the object interaction.
                
                :param fileToLoad: Path to the geo file
                :type fileToLoad: String

                :return: instantiated object
                :rtype: GeometryFile object
                """

                self.model = None

		self.position = None

                #: Changeing initial position or angle requires reset() call.
		self.initialAngles = [0, 0, 0]
                self.initialPosition = [0, 0, 0]

                #: Set maximum rotation here.
                #: TODO Not working so far
		self.xAngClamp = 90
		self.yAngClamp = 90
		self.zAngClamp = 90

                #: Set maximum translation here.
                self.xPosClamp = 1
                self.yPosClamp = 1
                self.zPosClamp = 1

                self.textured = True

		self.modelInfos = []

                self.loadModel(fileToLoad)

                self.reset()

        def reset(self):
                """Reset to original position.
                
                The rotation is reset inside the SceneNode, the reset position is read in updateModel().
                """
                self.model.setOrientation(quaternionFromEulerDeg(*self.initialAngles))
                self.position = self.initialPosition

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

                # translate newModel if getBoundCenter would work
		if newModel.getName() not in GeometryFile._offsets.keys():
			GeometryFile._offsets[newModel.getName()] = -newModel.getBoundCenter()
		newModel.initialPosition = GeometryFile._offsets[newModel.getName()]

                self.model = newModel

        def updateModel(self, newAngles, newPosition):
                """Callback for DAEventhandler to update coordinates.

                :param newAngle: Rotation vector
                :param newPosition: Translation vector
                :type newAngle: List with 3 double values
                :type newPosition: List with 3 double values

                This method is used to change the angle and position or the object with the given vectors
                """
                angles = [
                        min(max(newAngles[0], -self.xAngClamp), self.xAngClamp),
                        min(max(newAngles[1], -self.yAngClamp), self.yAngClamp),
                        min(max(newAngles[2], -self.zAngClamp), self.zAngClamp)
                ]

                self.model.setOrientation(quaternionFromEulerDeg(*angles) * self.model.getOrientation())

                self.position = [
                        min(max(self.position[0] + newPosition[0], -self.xPosClamp), self.xPosClamp),
                        min(max(self.position[1] + newPosition[1], -self.yPosClamp), self.yPosClamp),
                        min(max(self.position[2] + newPosition[2], -self.zPosClamp), self.zPosClamp)
                ]

                # update position to have newest pivot for rotation
                self.model.setPosition(Vector3(*self.position))
