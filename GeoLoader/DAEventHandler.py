from omega import getDefaultCamera, getEvent, ServiceType, EventFlags, EventType, isStereoEnabled, toggleStereo, quaternionFromEulerDeg
from daHEngine import HoudiniEngine

class DAEventHandler():
        """This class encapsulates the navigation interaction with geometry loaded into omegalib.

        An instance of DAEventHandler can load several `GemoetryFile` objects.
        The functions `onEvent()` and `onUpdate()` are registered at the omegalib callbacks.
        Interaction with the loaded objects is then provided via mouse, keyboard or Space Navigator.
        """
        def __init__(self):
                """The constructor provides several tuning parameters."""
                self.cam = getDefaultCamera()
                self.cameraControl = False
                self.initialCamRotation = self.cam.getOrientation()
                self.initialCamPosition = self.cam.getPosition()

                self.geos = []
                #: Sensitivity of the Space Navigator movement/rotation
                self.spaceNavMoveSensitivity = 5.0
                self.spaceNavRotSensitivity = 0.005

                self.controllerSensitivity = 3.0
                self.controllerDeadzone = 0.0
                self.controllerChannels = None

                self.leftButtonDown = False
                self.middleButtonDown = False
                self.rightButtonDown = False

                self.mousePos = None
                self.prevMousePos = None

                #:Mouse sensitivity
                self.xRotSensitivity = 0.3
                self.yRotSensitivity = 0.3
                self.zRotSensitivity = 0.3
                
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
                self.invertYMove = False
                self.invertZMove = True

                self.invertXRot = True
                self.invertYRot = True
                self.invertZRot = False

                self.allowStereoSetting = True

                self.printHelp()

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
                

        def addGeo(self, geo):
                """Registers a `GeometryFile` object."""
                self.geos.append(geo)

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
                        self.cameraControl = not self.cameraControl

                # set pitch and movement negative for intuitive movement and mouse compliance

                pitch = -e.getExtraDataFloat(3) * self.spaceNavMoveSensitivity
                yaw   = e.getExtraDataFloat(5) * self.spaceNavMoveSensitivity
                roll  = e.getExtraDataFloat(4) * self.spaceNavMoveSensitivity

                angles = [pitch, yaw, roll]

                x = -e.getExtraDataFloat(0) * self.spaceNavRotSensitivity
                y = -e.getExtraDataFloat(2) * self.spaceNavRotSensitivity
                z = -e.getExtraDataFloat(1) * self.spaceNavRotSensitivity

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
                        position[1] = yMove

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

        def onEvent(self):
                """Callback for omegalib to register with `setEventFunction`."""
                e = getEvent()
                angles = [0, 0, 0]
                position = [0, 0, 0]
                
                if self.allowStereoSetting:
                        if e.isKeyDown(ord('s')):
                                self.changeStereo()

                if e.isKeyDown(ord('m')):
                        self.cameraControl = not self.cameraControl

                if e.isKeyDown(ord('n')):
                        self.resetView()

                if e.isKeyDown(ord('i')):
                        self.printConfig()

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
                        self.cam.setOrientation(quaternionFromEulerDeg(*angles) * self.cam.getOrientation())
                        self.cam.setPosition(*(position + self.cam.getPosition()))
                else:
                        [ g.updateModel(angles, position) for g in self.geos ]

        def onUpdate(self, frame, time, dt):
                """Callback for omegalib to register with `setUpdateFunction`."""
                pass
#                self.doControllerMove()

        def resetView(self):
                """Resets the position of object or camera."""
                if self.cameraControl:
                        self.cam.setOrientation(self.initialCamRotation)
                        self.cam.setPosition(self.initialCamPosition)
                else:
                        [ g.reset() for g in self.geos ]

        def changeStereo(self):
                """Toggles stereo view and sets eye separation"""
                toggleStereo()
                if isStereoEnabled():
                        #getDisplayConfig().stereoMode = StereoMode.LineInterleaved
                        getDefaultCamera().setEyeSeparation(0.0007)
                else:
                        #getDisplayConfig().stereoMode = StereoMode.Mono
                        getDefaultCamera().setEyeSeparation(0.06)

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
                DAEventHandler.addGeo(self, otl)

                otlName, assetName, geoName = otl.otlDescription
                self.engine.loadAssetLibraryFromFile(otlName)
                self.engine.instantiateAsset(assetName)
                staticObject = self.engine.instantiateGeometry(geoName)
                otl.setModel(staticObject)

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



from euclid import Vector2, Vector3
from omega import Color, loadImage, SceneNode
from omegaToolkit import Container, ContainerLayout, Label, Image, UiModule

class CanvasHandler(DAEventHandler):

        def __init__(self):
                DAEventHandler.__init__(self)
                self.cursors = []
                self.distance = 0


                ui = UiModule.createAndInitialize()
                node = SceneNode.create("container")
                self.geos.append(node)

                self.container = Container.create(ContainerLayout.LayoutFree, ui.getUi())
                c3d = self.container.get3dSettings()
                c3d.enable3d = True
                c3d.position = Vector3(-4, 2.7, -3) # dablab
                c3d.scale = 0.001
                c3d.node = node

                self.cursorImg = loadImage('/da/sw/omegalib/myCursor.png')
                self.cursorClickImg = loadImage('/da/sw/omegalib/myCursor_click.png')

        def addGeo(self, canvas):
                """Loads canvas and set position in container."""
                #DAEventHandler.addGeo(self, canvas)

                # Update container size and position canvas
                width = canvas.width
                height = canvas.height
                self.container.setWidth(self.container.getWidth() + width + self.distance)
                if (self.container.getHeight() < height):
                    self.container.setHeight(height)

                canvas.initialPosition = [ self.container.getWidth() - width, 0, 0]
                canvas.setModel(self.container)

        def addCursor(self, name, color):
                cursor = Image.create(cont)
                label = Label.create(cont)
                label.setText(name)
                label.setFont('fonts/arial.ttf 18')
                label.setColor(Color('white'))
                label.setPosition(Vector2(32, 12))
                label.setFillEnabled(True)
                label.setFillColor(Color(color))

                if len(self.cursors) == 0:
                        cursor.setSize(Vector2(32, 32))
                        cursor.setData(cursorImg)
                else:
                        cursor.setData(loadImage('/da/sw/omegalib/myCursor_' + str(i + 1) + '.png'))
                        cursor.setSize(Vector2(24, 24))
                self.cursors.append((cursor, label))

        def diff(q1, q2):
                return ((abs(q2.w) + abs(q2.x) + abs(q2.y) + abs(q2.z)) -
                         (abs(q1.w) + abs(q1.x) + abs(q1.y) + abs(q1.z)))

        def onEvent():
                print "in canvas handler"
                DAEventHandler.onEvent(self)

                prevDiffAmt = 0.0
                prevOrientations = [[Quaternion()]] * len(self.cursors)

                e = getEvent()

                if e.getServiceType() == ServiceType.Mocap:
                        if e.getExtraDataItems() >= 2:
                                point = Vector2(e.getExtraDataInt(0), e.getExtraDataInt(1))
                                if e.getUserId() > len(self.cursors):
                                        return

                                #po = prevOrientations[e.getUserId() - 1]
                                po = Quaternion()

                                for a in prevOrientations[e.getUserId() - 1]:
                                        #a.w *= (1.0 / len(prevOrientations[e.getUserId() - 1]))
                                        #po *= a
                                        po.w += a.w
                                        po.x += a.x
                                        po.y += a.y
                                        po.z += a.z

                                po.w /= 1.0 * len(prevOrientations[e.getUserId() - 1])
                                po.x /= 1.0 * len(prevOrientations[e.getUserId() - 1])
                                po.y /= 1.0 * len(prevOrientations[e.getUserId() - 1])
                                po.z /= 1.0 * len(prevOrientations[e.getUserId() - 1])

                                aa = e.getOrientation()
                                diffAmt = diff(aa, po)

                                diffChange = abs(diffAmt - prevDiffAmt)

                                # TODO use change in diff from average of previous quats to compare against
                                if diffChange < 0.075:
                                        print "diff change:", diffChange
#                                        cursors[e.getUserId() - 1].setPosition(point)
#                                        labels[e.getUserId() - 1].setPosition(point + Vector2(32, 12))

                                prevDiffAmt = diffAmt

                                prevOrientations[e.getUserId() - 1].append(e.getOrientation())
                                if len(prevOrientations[e.getUserId() - 1]) >= 4:
                                        prevOrientations[e.getUserId() - 1].pop(0)

                        if (e.getUserId() == 1):
                                vec = e.getOrientation() * Vector3(0, 1, 0)

                                if vec[1] < -0.6:
                                        self.cursors[e.getUserId() - 1][0].setData(self.cursorClickImg)
                                else:
                                        self.cursors[e.getUserId() - 1][0].setData(self.cursorImg)
