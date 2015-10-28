from euclid import Vector3
from omega import getDefaultCamera, getEvent, ServiceType, EventFlags, EventType, isStereoEnabled, toggleStereo, Space, quaternionFromEulerDeg

class DAEventHandler():

        def __init__(self):
                self.cam = getDefaultCamera()
                self.cameraControl = False
                self.initialCamAngles = self.cam.getOrientation()
                self.initialCamPosition = self.cam.getPosition()

                self.geos = []

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

                # mouse sensitivity
                self.xAngSensitivity = 0.3
                self.yAngSensitivity = 0.3
                self.zAngSensitivity = 0.3
                
                self.xPosSensitivity = 0.004
                self.yPosSensitivity = 0.004
                self.zPosSensitivity = 0.004

                # navigation restriction
                self.allowXMove = True
                self.allowYMove = True
                self.allowZMove = True

                self.allowXRot = True
                self.allowYRot = True
                self.allowZRot = True

                # change direction of movement
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
                print "Use Ctrl+[x,y,z, p,j,r] to invert the direction of movement/rotation in the selected axis"
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
                self.geos.append(geo)

        # Space Navigator axes:
        #0 (-left, +right)
        #1 (-forward, +back)
        #2 (-up, +down)
        #3 pitch (-forward, +back)
        #4 roll (-right, +left)
        #5 yaw (-left, +right)
        def onSpaceNavEvent(self, e):
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

        # TODO: integrate PS controller
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

                        xMove = self.xPosSensitivity * delta.x
                        yMove = self.yPosSensitivity * delta.y

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

                        xDeg = self.xAngSensitivity * delta.x
                        yDeg = self.yAngSensitivity * delta.y

                        angles[1] = xDeg
                        angles[0] = yDeg

                        self.prevMousePos = e.getPosition()

                elif e.isButtonDown(EventFlags.Middle):
                        self.middleButtonDown = True
                        self.mousePos = e.getPosition()
                        self.prevMousePos = self.mousePos

                elif e.isButtonUp(EventFlags.Middle):
                        self.middleButtonDown = False

                elif self.middleButtonDown and e.getType() == EventType.Move:
                        delta = self.prevMousePos - e.getPosition()
                        
                        zAng = self.zAngSensitivity * delta.x
                        zMove = self.zPosSensitivity * delta.y

                        angles[2] = zAng
                        position[2] = zMove 

                        self.prevMousePos = e.getPosition()

                return angles, position

        def restrictControl(self, event):
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
                        self.cam.setOrientation(self.cam.getOrientation() * quaternionFromEulerDeg(*angles))
                        self.cam.translate(Vector3(*position), Space.Local)
                else:
                        [ g.updateModel(angles, position) for g in self.geos ]

        def onUpdate(self, frame, time, dt):
                pass
#                self.doControllerMove()

        def resetView(self):
                if self.cameraControl:
                        self.cam.setOrientation(self.initialCamAngles)
                        self.cam.setPosition(self.initialCamPosition)
                else:
                        [ g.reset() for g in self.geos ]

        def changeStereo(self):
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
