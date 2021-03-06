"""The module provides classes for different visualizations in the Data Arena."""

try:
    from omega import SceneNode, quaternionFromEulerDeg, Space
except ImportError:
    print "Could not import module: omega."
try:
    from euclid import Vector3
except ImportError:
    print "Could not import module: euclid."
try:
    from cyclops import ModelInfo, StaticObject, getSceneManager
except ImportError:
    print "Could not import module: cyclops."
try:
    from omega import isMaster, PixelData, PixelFormat, ImageFormat
    from omegaToolkit import ImageBroadcastModule, Image
except ImportError:
    print "Could not import modules for Canvas."


class BaseObject():
    """The class provides a base wrapper for objects of Data Arena visualizations."""

    def __init__(self):
        """The constructor provides some parameters to tune the object interaction."""

        self.model = None

        #: Changing initial position/rotation requires reset() call.
        self.initialRotation = [0, 0, 0]
        self.initialPosition = [0, 0, 0]

        #: Specifies rotation point of the object, requires reset(). (default: center of bounding box)
        self.pivotPoint = [0, 0, 0]

    def reset(self):
        """Reset to initial position."""
        pass

    def updateModel(self, newRotation, newPosition):
        """Callback for Handler to update position and orientation.

        :param newRotation: Rotation vector
        :param newPosition: Translation vector
        :type newRotation: List with 3 double values
        :type newPosition: List with 3 double values

        This method is used to change the angle and position or the object with the given vectors
        """
        pass


class Geometry(BaseObject):
    """The class provides a wrapper to load a geometry file into omegalib.

    An instantiated object is registered at a `GeometryHandler` object and encapsulates the geometry.
    """

    createdInstances = {}

    def __init__(self, fileToLoad=""):
        """The constructor provides some parameters to tune the object interaction.

        :param fileToLoad: Path to the geo file
        :type fileToLoad: String

        :return: instantiated object
        :rtype: Geometry object
        """

        BaseObject.__init__(self)

        self.cameraPosition = [0, 0, 0]

        #: Set maximum rotation here.
        #: TODO Not working so far, see updateModel()
        self.xRotClamp = 90
        self.yRotClamp = 90
        self.zRotClamp = 90

        #: Set maximum translation here.
        self.xMoveClamp = 10
        self.yMoveClamp = 10
        self.zMoveClamp = 10

        self.textured = True

        self.modelInfos = []

          

        if fileToLoad != "":
            self.loadModel(fileToLoad)
            self.reset()

    def reset(self):
        """Reset to initial position.

        Update pivot point and set configured initialRotation/Position, redraw with updateModel().
        """

        if self.model is None:
            return

        self.model.getChildByIndex(0).setPosition(*self.pivotPoint)

        self.model.setPosition(*self.initialPosition)
        self.model.setOrientation(
            quaternionFromEulerDeg(*self.initialRotation))

    def loadModel(self, fileToLoad):
        """Loads a geometry model from the given file.

        :param fileToLoad: Path to geo file
        """

        modelName = self._makeName(fileToLoad)
        print "model:", modelName

        modelInfo = ModelInfo()

        modelInfo.name = modelName
        modelInfo.path = fileToLoad
        # optimising takes a LONG time..
        modelInfo.optimize = False
        self.modelInfos.append(modelInfo)

        getSceneManager().loadModel(modelInfo)

        newModel = StaticObject.create(modelName)
        newModel.setName(modelName)

        if self.textured:
            newModel.setEffect("textured")
            newModel.setEffect("@unlit")
        else:
            newModel.setEffect("colored -d white -C")

        newModel.getMaterial().setDoubleFace(True)

        self.pivotPoint = list(-newModel.getBoundCenter())

        #: Use parent object to apply correct rotation on initially translated objects.
        self.model = SceneNode.create("ParentOf_" + modelName)
        self.model.addChild(newModel)

    def _makeName(self, fileToLoad):
        if Geometry.createdInstances.has_key(fileToLoad):
            Geometry.createdInstances[fileToLoad]+=1
            return fileToLoad+str(Geometry.createdInstances[fileToLoad])
        else:
            Geometry.createdInstances[fileToLoad] = 1
        
        return fileToLoad

    def setPosition(self, position):
        """ Set model to position.

        :param position: A 3-tuple or list """
        # self.model.
        self.model.setPosition(*position)

    def setModel(self, modelGeometry):
        """Sets the object to have the given geometry

        :param modelGeometry: ModelGeometry, should not have been added to the scene yet
        """

        getSceneManager().addModel(modelGeometry)
        newModel = StaticObject.create(modelGeometry.getName())
        newModel.setName(modelGeometry.getName())

        self.pivotPoint = list(-newModel.getBoundCenter())

        #: Use parent object to apply correct rotation on initially translated objects.
        self.model = SceneNode.create("ParentOf_" + modelGeometry.getName())
        self.model.addChild(newModel)

    def setStaticObject(self, staticObject):
        """Sets the object to have the given asset

        :param staticObject: staticObject, should not have been added to the scene yet
        """
        self.pivotPoint = list(-staticObject.getBoundCenter())

        #: Use parent object to apply correct rotation on initially translated objects.
        self.model = SceneNode.create("ParentOf_StaticObject")#TODO set correct name
        self.model.addChild(staticObject)

    def setShader(self, program):
        getSceneManager().addProgram(program)
        self.getMaterial().setProgram(program.name)

    def getMaterial(self):
        return self.model.getChildByIndex(0).getMaterial()

    def updateModel(self, newRotation, newPosition):
        # TODO: clamping the rotation does not work with Quaternions, omegalib conversion seems not precise
        # First try: convert quaternion to euler, clamp and apply result
        # Result: Object moves around without dragging (rounded conversiona?)
        # second try: only apply new rotation if total converted rotation is in interval
        # Result: Sometimes box is moving without interaction
        #       converted eulerDeg are different for same rotation which results in more rotation than allowed
        #

        if self.model is None:
            return

        angles = [
            min(max(newRotation[0], -self.xRotClamp), self.xRotClamp),
            min(max(newRotation[1], -self.yRotClamp), self.yRotClamp),
            min(max(newRotation[2], -self.zRotClamp), self.zRotClamp)
        ]

        # use world space, since camera always aligned with that
        self.model.rotate(Vector3(1, 0, 0), angles[0], Space.World)
        self.model.rotate(Vector3(0, 1, 0), angles[1], Space.World)
        self.model.rotate(Vector3(0, 0, 1), angles[2], Space.World)

        oldPosition = self.model.getPosition()
        position = [0, 0, 0]
        for i in range(0, 3):
            position[i] = oldPosition[i] + \
                newPosition[i] - self.cameraPosition[i]

        if position[0] > self.xMoveClamp or position[0] < -self.xMoveClamp:
            newPosition[0] = 0
        if position[1] > self.yMoveClamp or position[1] < -self.yMoveClamp:
            newPosition[1] = 0
        if position[2] > self.zMoveClamp or position[2] < -self.zMoveClamp:
            newPosition[2] = 0

        self.model.translate(Vector3(*newPosition), Space.World)

class OTL(Geometry):
    """Encapsulates an OTL to load it into omegalib with an OTLHandler."""

    def __init__(self, otlDescription):
        """Initialize empty Geometry object.

        :param otlDescription: Information of the OTL to load later.
        :type otlDescription: Tripel: OTL filename, OTL object name, geometry name)
        """
        Geometry.__init__(self, None)
        self.otlDescription = otlDescription

    def loadModel(self, otlDescription):
        self.modelInfos = None

    def setModel(self, staticObject):
        """Called from OTLHanlder to add model provided from HoudiniEngine."""
        self.pivotPoint = list(-staticObject.getBoundCenter())

        #: Use parent object to apply correct rotation on initially translated objects.
        self.model = SceneNode.create("Parent")
        self.model.addChild(staticObject)
        self.reset()


class Canvas(BaseObject):
    """Encapsulates a webpage"""

    def __init__(self, url, width, height):
        #[max] The reason to shift the import here is to prevent an error loading the gconf library
        # silently mess up loading other libraries. Therefore purposfully crash, if the import fails
        from webView import WebView, WebFrame


        """Initialize new webpage with filename or URL."""
        # not necessary to call super class
        self.url = url
        self.width = width
        self.height = height
        # Vector2 set from Handler
        self.position = None

    def setModel(self, container):
        """Called from Handler to add data in container."""
        frame = None
        view = None
        if isMaster():
            view = WebView.create(self.width, self.height)
            view.loadUrl(self.url)
            frame = WebFrame.create(container)
            frame.setView(view)
        else:
            view = PixelData.create(
                self.width, self.height, PixelFormat.FormatRgba)
            frame = Image.create(container)
            frame.setDestRect(0, 0, self.width, self.height)
            frame.setData(view)
        frame.setPosition(self.position)
        ImageBroadcastModule.instance().addChannel(
            view, self.url, ImageFormat.FormatNone)
        #self.model = container.get3dSettings().node
