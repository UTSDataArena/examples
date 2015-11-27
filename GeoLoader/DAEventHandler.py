from omega import getDefaultCamera, getEvent, ServiceType, EventFlags, EventType, isStereoEnabled, toggleStereo, quaternionFromEulerDeg, SceneNode
from euclid import Vector3

class DAEventHandler():
        """This class encapsulates the navigation interaction with geometry loaded into omegalib.

        An instance of DAEventHandler can load several `GemoetryFile` objects.
        The functions `onEvent()` and `onUpdate()` are registered at the omegalib callbacks.
        Interaction with the loaded objects is then provided via mouse, keyboard or Space Navigator.

        self.objects and self.cameraObject stay always on position [0,0,0] which is the pivot point for the camera.
        Instead of moving the camera, all objects in self.objects are moved.
        Rotation is applied either on cameraObject (in cameraControl) or self.objects.
        This aligns the view always with the intuitive coordinat system (x: horizontal, y: vertical, z: depth).
        """
        def __init__(self):
                """The constructor provides several tuning parameters."""
                self.geos = []
                self.currentModel = -1
                #: Parent all objects to apply camera rotation, while camera stays the same.
                self.objects = SceneNode.create("objects")

                defCam = getDefaultCamera()
                defCam.setControllerEnabled(False)
                defCam.setNearFarZ(0.001, 1000)
                defCam.setPosition(-defCam.getHeadOffset())

                #: Absolute position and orientation of camera, headOffset is substracted.
                #: View in negative Z
                self.initialCamRotation = [0, 0, 0]
                self.initialCamPosition = [0, 0, 0]

                #: Parent camera to abstract from headOffset
                self.cameraObject = SceneNode.create("Camera")
                self.cameraObject.addChild(defCam)

                self.cameraControl = False

                #: Sensitivity of the Space Navigator movement/rotation
                self.spaceNavMoveSensitivity = 0.05
                self.spaceNavRotSensitivity = 0.05

                self.controllerSensitivity = 3.0
                self.controllerDeadzone = 0.0
                self.controllerChannels = None

                self.leftButtonDown = False
                self.middleButtonDown = False
                self.rightButtonDown = False

                self.mousePos = None
                self.prevMousePos = None

                #:Mouse sensitivity
                self.xRotSensitivity = 0.004
                self.yRotSensitivity = 0.004
                self.zRotSensitivity = 0.004
                
                self.xMoveSensitivity = 0.004
                self.yMoveSensitivity = 0.004
                self.zMoveSensitivity = 0.004

                #: Navigation restriction
                self.allowXMove = True
                self.allowYMove = True
                self.allowZMove = True

                self.allowXRot = True
                self.allowYRot = True
                self.allowZRot = True

                #: Invert direction of movement
                self.invertXMove = True
                self.invertYMove = True
                self.invertZMove = True

                self.invertXRot = True
                self.invertYRot = True
                self.invertZRot = True

                self.allowStereoSetting = True

                self.printHelp()

        def addGeo(self, geo):
                """Registers a `GeometryFile` object."""
                self.geos.append(geo)
                self.objects.addChild(geo.model)
                geo.cameraPosition = -Vector3(*self.initialCamPosition)
                # position objects relative to camera
                self.resetView()

        def printHelp(self):
                print "\n=========================\n"
                print "Use keys x,y,z to toggle object movement on axis x,y or z"
                print 
                print "Use keys p,j,r to toggle object rotation on axis x,y or z (pitch, jam jar, roll)"
                print
                print "Use Shift+[x,y,z, p,j,r] to invert the direction of movement/rotation in the selected axis"
                print
                print "Use key m to toggle camera or object control mode"
                print
                print "Use key n to reset the view"
                print
                print "Use key s to toggle stereo view"
                print
                print "Use key i to print active configuration"
                print "\n=========================\n"

        def printConfig(self):
                """Prints the current configuration of important parameters."""
                stringConvert = {True:'enabled', False:'disabled'}
                print "\n=========================\n"
                print "Stereo is %s" % stringConvert[isStereoEnabled()]
                if self.cameraControl: 
                        print "You control the camera!"
                else:
                        print "You control the object!"
                print
                print "Movement on x axis is %s" % stringConvert[self.allowXMove]
                print "Movement on y axis is %s" % stringConvert[self.allowYMove]
                print "Movement on z axis is %s" % stringConvert[self.allowZMove]
                print
                print "Rotation on x axis is %s" % stringConvert[self.allowXRot]
                print "Rotation on y axis is %s" % stringConvert[self.allowYRot]
                print "Rotation on z axis is %s" % stringConvert[self.allowZRot]
                print "\n=========================\n"
                
        # Space Navigator axes:
        #0 (-left, +right)
        #1 (-forward, +back)
        #2 (-up, +down)
        #3 pitch (-forward, +back)
        #4 roll (-right, +left)
        #5 yaw (-left, +right)
        def onSpaceNavEvent(self, e):
                """Callback for `onEvent` to read Space Navigator input."""
                if e.isButtonDown(EventFlags.Button1):
                        self.resetView()
                if e.isButtonDown(EventFlags.Button2):
                        self.toggleView()

                # set pitch, roll and x,z movement negative for intuitive movement
                pitch = -e.getExtraDataFloat(3) * self.spaceNavRotSensitivity
                yaw   = e.getExtraDataFloat(5) * self.spaceNavRotSensitivity
                roll  = -e.getExtraDataFloat(4) * self.spaceNavRotSensitivity
                if self.cameraControl:
                    pitch = -pitch
                    yaw = -yaw
                    roll = -roll

                angles = [pitch, yaw, roll]

                x = -e.getExtraDataFloat(0) * self.spaceNavMoveSensitivity
                y = e.getExtraDataFloat(2) * self.spaceNavMoveSensitivity
                z = -e.getExtraDataFloat(1) * self.spaceNavMoveSensitivity

                position = [x, y, z]

                return angles, position

        #: TODO: integrate PS controller
        # ps3, ps4 and ps move Controller controls
        # Left analog:
        # channel 0: left/right - yaw
        # channel 1: up/down 	 - zoom
        # Right analog:
        # channel 2: left/right -
        # channel 3: up/down 	 - pan y
        def onGameControllerEvent(self, e):
                self.controllerChannels = map(e.getExtraDataFloat, range(6))

                for i in range(len(self.controllerChannels)):
                        if abs(self.controllerChannels[i]) < self.controllerDeadzone:
                                self.controllerChannels[i]=0

        # repeats movement without incomming events
        def doControllerMove(self):
                if not self.controllerChannels:
                        return

                pitch = 0
                yaw  = self.controllerChannels[0] * self.controllerSensitivity
                roll  = 0

                #x = e.getExtraDataFloat(0) * self.controllerSensitivity * 0.05
                x = 0
                y = -self.controllerChannels[3] * self.controllerSensitivity * 0.001
                z = self.controllerChannels[1] * self.controllerSensitivity * 0.005

                angles = [pitch, yaw, roll]

                position = [x, y, z]
                return angles, position

        def onMouseEvent(self, e):
                """Callback for `onEvent` to read Mouse input."""
                angles = [0, 0, 0]
                position = [0, 0, 0]
                if e.isButtonDown(EventFlags.Left):
                        self.leftButtonDown = True
                        self.mousePos = e.getPosition() #pixel coordinates
                        self.prevMousePos = self.mousePos

                elif e.isButtonUp(EventFlags.Left):
                        self.leftButtonDown = False

                elif self.leftButtonDown and e.getType() == EventType.Move:
                        delta = self.prevMousePos - e.getPosition()

                        xMove = self.xMoveSensitivity * delta.x
                        yMove = self.yMoveSensitivity * delta.y

                        position[0] = xMove
                        # Make it negative for intuitive movement
                        position[1] = -yMove

                        self.prevMousePos = e.getPosition()

                # right mouse button
                elif e.isButtonDown(EventFlags.Right):
                        self.rightButtonDown = True
                        self.mousePos = e.getPosition()
                        self.prevMousePos = self.mousePos

                elif e.isButtonUp(EventFlags.Right):
                        self.rightButtonDown = False

                elif self.rightButtonDown and e.getType() == EventType.Move:
                        delta = self.prevMousePos - e.getPosition()

                        # swap axis for intuitive mouse movement
                        xDeg = self.xRotSensitivity * delta.y
                        yDeg = self.yRotSensitivity * delta.x

                        angles[0] = xDeg
                        angles[1] = yDeg

                        self.prevMousePos = e.getPosition()

                elif e.isButtonDown(EventFlags.Middle):
                        self.middleButtonDown = True
                        self.mousePos = e.getPosition()
                        self.prevMousePos = self.mousePos

                elif e.isButtonUp(EventFlags.Middle):
                        self.middleButtonDown = False

                elif self.middleButtonDown and e.getType() == EventType.Move:
                        delta = self.prevMousePos - e.getPosition()
                        
                        zRot = self.zRotSensitivity * delta.x
                        zMove = self.zMoveSensitivity * delta.y

                        angles[2] = zRot
                        position[2] = zMove 

                        self.prevMousePos = e.getPosition()

                return angles, position

        def onEvent(self):
                """Callback for omegalib to register with `setEventFunction`."""
                e = getEvent()
                angles = [0, 0, 0]
                position = [0, 0, 0]
                
                if self.allowStereoSetting:
                        if e.isKeyDown(ord('s')):
                                self.changeStereo()

                if e.isKeyDown(ord('m')):
                        self.toggleView()

                if e.isKeyDown(ord('n')):
                        self.resetView()

                if e.isKeyDown(ord('i')):
                        self.printConfig()

                if e.isKeyDown(ord('>')):
                        self.nextModel()

                if e.getServiceType() == ServiceType.Controller:
                    if e.getSourceId() == 1:
                            # space navigator
                            angles, position = self.onSpaceNavEvent(e)
                    elif e.getSourceId() == 0:
                            angles, position = self.onGameControllerEvent(e)

                if e.getServiceType() == ServiceType.Pointer:
                        angles, position = self.onMouseEvent(e)

                self.restrictControl(e)
                angles, position = self.applyRestriction(angles, position)
                angles, position = self.invertNavigation(e, angles, position)

                if self.cameraControl:
                        self.cameraObject.setOrientation( \
                             self.cameraObject.getOrientation() * quaternionFromEulerDeg(*angles))
                        # no rotation of objects anymore
                        angles = [0, 0, 0]
                        # but include rotation in translation
                        position = self.cameraObject.getOrientation() * Vector3(*position)

                [ g.updateModel(angles, position) for g in self.geos ]

        def onUpdate(self, frame, time, dt):
                """Callback for omegalib to register with `setUpdateFunction`."""
                pass
#                self.doControllerMove()

        def restrictControl(self, event):
                """Restricts movement on axes.

                On specified keyboard events the movement or rotation of the object, respectively camera, is blocked.
                """
                if event.isKeyDown(ord('x')):
                        self.allowXMove = not self.allowXMove
                if event.isKeyDown(ord('y')):
                        self.allowYMove = not self.allowYMove
                if event.isKeyDown(ord('z')):
                        self.allowZMove = not self.allowZMove
                if event.isKeyDown(ord('p')):
                        self.allowXRot = not self.allowXRot
                if event.isKeyDown(ord('j')):
                        self.allowYRot = not self.allowYRot
                if event.isKeyDown(ord('r')):
                        self.allowZRot = not self.allowZRot

        def applyRestriction(self, angles, position):
                if not self.allowXRot:
                    angles[0] = 0
                if not self.allowYRot:
                    angles[1] = 0
                if not self.allowZRot:
                    angles[2] = 0

                if not self.allowXMove:
                    position[0] = 0
                if not self.allowYMove:
                    position[1] = 0
                if not self.allowZMove:
                    position[2] = 0

                return angles, position

        def invertNavigation(self, event, angles, position):
                if event.isKeyDown(ord('X')):
                        self.invertXMove = not self.invertXMove
                if self.invertXMove:
                         position[0] = -position[0]

                if event.isKeyDown(ord('Y')):
                        self.invertYMove = not self.invertYMove
                if self.invertYMove:
                         position[1] = -position[1]

                if event.isKeyDown(ord('Z')):
                        self.invertZMove = not self.invertZMove
                if self.invertZMove:
                         position[2] = -position[2]

                if event.isKeyDown(ord('P')):
                        self.invertXRot = not self.invertXRot
                if self.invertXRot:
                         angles[0] = -angles[0]

                if event.isKeyDown(ord('J')):
                        self.invertYRot = not self.invertYRot
                if self.invertYRot:
                         angles[1] = -angles[1]

                if event.isKeyDown(ord('R')):
                        self.invertZRot = not self.invertZRot
                if self.invertZRot:
                         angles[2] = -angles[2]

                return angles, position

        def getCamera(self):
                """Returns the camera of the scene.

                Getter necessary because of parented camera object.
                This is done to correctly implement rotation of translated objects.
                Allows to ajust camera parameters, such as clipping planes or eye separation.
                """
                return self.cameraObject.getChildByIndex(0)

        def changeStereo(self):
                """Toggles stereo view and sets eye separation"""
                toggleStereo()
                if isStereoEnabled():
                        #getDisplayConfig().stereoMode = StereoMode.LineInterleaved
                        self.getCamera().setEyeSeparation(0.0007)
                else:
                        #getDisplayConfig().stereoMode = StereoMode.Mono
                        self.getCamera().setEyeSeparation(0.06)

        def resetView(self):
                """Resets the position and orientation of object and camera."""
                if self.cameraControl:
                    self.cameraObject.setOrientation(quaternionFromEulerDeg(*self.initialCamRotation))
                    self.objects.resetOrientation()
                    cameraOffset = -Vector3(*self.initialCamPosition)
                else:
                    self.cameraObject.resetOrientation()
                    cameraRotation = quaternionFromEulerDeg(*self.initialCamRotation).conjugated()
                    self.objects.setOrientation(cameraRotation)
                    cameraOffset = cameraRotation * -Vector3(*self.initialCamPosition)

                for g in self.geos:
                    g.reset()
                    # move objects invers of initial camera position
                    g.updateModel([0,0,0], cameraOffset)

        def toggleView(self):
                """Toggles between object and camera control."""
                self.cameraControl = not self.cameraControl
                self.adjustSensitivity()
                if self.cameraControl:
                    self.cameraObject.setOrientation(self.objects.getOrientation().conjugated())
                    self.objects.resetOrientation()
                else:
                    self.objects.setOrientation(self.cameraObject.getOrientation().conjugated())
                    self.cameraObject.resetOrientation()

                self.invertXMove = not self.invertXMove
                self.invertYMove = not self.invertYMove
                self.invertZMove = not self.invertZMove
                self.invertXRot = not self.invertXRot
                self.invertYRot = not self.invertYRot
                self.invertZRot = not self.invertZRot

        def adjustSensitivity(self):
                """Sensitivity is lower for camera rotation."""
                if self.cameraControl:
                    self.xRotSensitivity *= 10
                    self.yRotSensitivity *= 10
                    self.zRotSensitivity *= 10
                    self.spaceNavRotSensitivity *= 10
                else:
                    self.xRotSensitivity /= 10
                    self.yRotSensitivity /= 10
                    self.zRotSensitivity /= 10
                    self.spaceNavRotSensitivity /= 10

        def nextModel(self):
                """Displays one model at a time.

                When more than one model is loaded, the first call just displays the first model.
                After that the models are swapped around.
                """
                if len(self.geos) <= 1: return

                if self.currentModel == -1:
                    # hide all models on first call
                    self.currentModel = len(self.geos) - 1
                    for i in range(0, len(self.geos)):
                        self.geos[i].model.getChildByIndex(0).setVisible(False)
                    self.nextModel()
                    return
                # then show one model after another
                self.geos[self.currentModel].model.getChildByIndex(0).setVisible(False)
                self.currentModel += 1
                if self.currentModel >= len(self.geos):
                    self.currentModel = 0
                self.geos[self.currentModel].model.getChildByIndex(0).setVisible(True)

from daHEngine import HoudiniEngine

class OTLHandler(DAEventHandler):

        def __init__(self):
                """Initializes DAEventHandler and HoudiniEngine."""
                DAEventHandler.__init__(self)
                self.engine = HoudiniEngine.createAndInitialize()
                self.engine.setLoggingEnabled(False)
                self.framesPerSec = 25
                self.play = False

        def addGeo(self, otl):
                """Loads OTL with HoudiniEngine."""
                otlName, assetName, geoName = otl.otlDescription
                self.engine.loadAssetLibraryFromFile(otlName)
                self.engine.instantiateAsset(assetName)
                staticObject = self.engine.instantiateGeometry(geoName)
                otl.setModel(staticObject)

                DAEventHandler.addGeo(self, otl)

        def renderFrame(self, frame):
                self.engine.setTime(frame / self.framesPerSec)
                self.engine.cook()

        def nextFrame(self, offset = 0):
                seconds = self.engine.getTime()
                self.renderFrame(seconds * self.framesPerSec + 1 + offset)

        def onUpdate(self, frame, time, dt):
                """Callback for omegalib to register with `setUpdateFunction`."""
                if self.play:
                    self.nextFrame()

        def onEvent(self):
                """Callback for omegalib to register with `setEventFunction`."""
                DAEventHandler.onEvent(self)

                e = getEvent()
                if e.isKeyDown(ord('f')):
                        self.nextFrame()
                if e.isKeyDown(ord('F')):
                        self.nextFrame(self.framesPerSec)
                if e.isKeyDown(ord('b')):
                        self.nextFrame(-2)
                if e.isKeyDown(ord('B')):
                        self.nextFrame(-self.framesPerSec -1)
                if e.isKeyDown(ord(' ')):
                        self.play = not self.play
