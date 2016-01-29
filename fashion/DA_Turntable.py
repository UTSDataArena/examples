#
# Turntable script
#
# [Darren 26Feb15]
#
# left click    			- rotate object around
# middle click  			- pan object
# right click   			- zoom object
#
# space navigator:
# forward/backward			- zoom
# up/down					- pan
# yaw						- rotate about Y axis
#
# controller:
# Left joystick	left/right	- rotate around Y
# Left joystick	up/down		- zoom
# Right joystick up/down	- pan
#
#
# model will start to rotate after idleTime seconds of no manual rotation
# model can be set to rotate and pan up/down by using the onUpdateDemo callback
#
# [Darren 29Jan16]
#
# Added to DAVM examples
#

from math import *
from euclid import *
from omega import *
from cyclops import *

class Turntable():
	_turntableCount = 0
	allowStereoSetting = False

	def makeBase(self):
		self.base = SceneNode.create("TurntableBase_" + str(Turntable._turntableCount))
		self.initialRot = self.base.getOrientation()
		self.angles = list(self.base.getOrientation().get_euler())
		self.basePos = list(self.base.getPosition())
		Turntable._turntableCount += 1

	def __init__(self):
		self.base = None

		self.leftButtonDown = False
		self.middleButtonDown = False
		self.rightButtonDown = False

		self.mousePos = None
		self.prevMousePos = None
		self.initialRot = None
		self.initialZoom = 2.0
		self.initialPan = None

		self.xSensitivity = 0.7
		#self.ySensitivity = 0.4
		self.spaceNavSensitivity = 5.0

		self.controllerSensitivity = 3.0
		self.controllerDeadzone = 0.0
		self.controllerChannels = None

		self.minZoomDist = 0.001
		self.maxZoomDist = 3.0

		self.panPos = getDefaultCamera().getHeadOffset().y

		self.idleTime = 5.0
		self.timeSinceEvent = 0.0
		self.spinSpeed = 1.0

		self.angles = None
		self.basePos = None
		self.xClamp = 0
		self.zClamp = 0

		self.minPanY = -0.5
		self.maxPanY = 3

		self.modelInfos = []

		self.offsets = {}

		self.makeBase()


	def addModel(self, fileToLoad):
		# Load a static model
		mdlModel = ModelInfo()
		mdlModel.name = fileToLoad
		mdlModel.path = fileToLoad
		mdlModel.size = 1.0
		mdlModel.optimize=False # optimising takes a LONG time..
		self.modelInfos.append(mdlModel)
		return self.modelInfos[-1]


	def loadModel(self, fileToLoad):
		getSceneManager().loadModel(self.addModel(fileToLoad))
		newModel = StaticObject.create(fileToLoad)
		newModel.setName(fileToLoad)
		self.setModel(newModel)


	def setModel(self, model):
		model.setEffect("textured-emissive")
		model.getMaterial().setColor(Color(1, 1, 1, 1), Color(1, 1, 1, 1))
		model.getMaterial().setDoubleFace(True)

		self.base.addChild(model)

		if model.getName() not in self.offsets.keys():
			model.setPosition(Vector3(0,0,0))
			self.offsets[model.getName()] = -model.getBoundCenter()

		model.translate(self.offsets[model.getName()], Space.Local)

	def unsetModel(self):
		while self.base.numChildren() > 0:
			self.base.removeChildByIndex(0)


	# Space Navigator axes:
	#0 (-left, +right)
	#1 (-forward, +back)
	#2 (-up, +down)
	#3 pitch (-forward, +back)
	#4 roll (-right, +left)
	#5 yaw (-left, +right)
	def onSpaceNavEvent(self, e):
		pitch = e.getExtraDataFloat(3) * self.spaceNavSensitivity
		yaw  = -e.getExtraDataFloat(5) * self.spaceNavSensitivity
		roll  = e.getExtraDataFloat(4) * self.spaceNavSensitivity

		self.angles = [
			self.angles[0] + pitch,
			self.angles[1] + yaw,
			self.angles[2] + roll
		]
		# clamping angles
		self.angles = [
			min(max(self.angles[0], -self.xClamp), self.xClamp),
			self.angles[1],
			min(max(self.angles[2], -self.zClamp), self.zClamp),
		]

		x = e.getExtraDataFloat(0) * self.spaceNavSensitivity * 0.05
		y = -e.getExtraDataFloat(2) * self.spaceNavSensitivity * 0.001
		z = e.getExtraDataFloat(1) * self.spaceNavSensitivity * 0.005

		self.basePos = [
			self.basePos[0] + x,
			self.basePos[1] + y,
			self.basePos[2] + z,
		]

		self.basePos = [
			min(max(self.basePos[0], 0.0), 0.0),
			min(max(self.basePos[1], -0.5), 3),
			min(max(self.basePos[2], self.minZoomDist), self.maxZoomDist),
		]

		self.base.setPosition(Vector3(*self.basePos))
		self.base.translate(0, y, 0, Space.Local)

		self.base.setOrientation(self.initialRot * quaternionFromEulerDeg(*self.angles))
		self.timeSinceEvent = 0


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

		self.timeSinceEvent = 0


	def onMouseEvent(self, e):
		if e.isButtonDown(EventFlags.Left):
			self.leftButtonDown = True
			self.mousePos = e.getPosition() #pixel coordinates
			self.prevMousePos = self.mousePos
			#self.initialRot = self.base.getOrientation()
			self.timeSinceEvent = 0
		elif e.isButtonUp(EventFlags.Left):
			self.leftButtonDown = False
			self.timeSinceEvent = 0

		elif self.leftButtonDown and e.getType() == EventType.Move:
			delta = self.prevMousePos - e.getPosition()
			xDeg = -self.xSensitivity * delta.x
			#yDeg = self.ySensitivity * delta.y
			#yDeg = min(max(yDeg, -60), 80)

			self.angles = [
				self.angles[0],
				self.angles[1] + xDeg,
				self.angles[2]
			]

			self.base.setOrientation(self.initialRot * quaternionFromEulerDeg(*self.angles))
			self.prevMousePos = e.getPosition()
			self.timeSinceEvent = 0

		elif e.isButtonDown(EventFlags.Right):
			self.rightButtonDown = True
			self.mousePos = e.getPosition()
			self.prevMousePos = self.mousePos

		elif e.isButtonUp(EventFlags.Right):
			self.rightButtonDown = False

		elif self.rightButtonDown and e.getType() == EventType.Move:
			delta = self.prevMousePos - e.getPosition()
			zoomAmt = -0.001 * delta.y
			camZ = getDefaultCamera().getPosition().z

			self.basePos[2] = min(max(self.basePos[2] + zoomAmt, camZ - self.maxZoomDist), camZ - self.minZoomDist)

			self.base.setPosition(*self.basePos)
			self.prevMousePos = e.getPosition()

		elif e.isButtonDown(EventFlags.Middle):
			self.middleButtonDown = True
			self.mousePos = e.getPosition()
			self.prevMousePos = self.mousePos

		elif e.isButtonUp(EventFlags.Middle):
			self.middleButtonDown = False

		elif self.middleButtonDown and e.getType() == EventType.Move:
			delta = self.prevMousePos - e.getPosition()
			panAmt = -0.0025 * delta.y

			self.basePos[1] = min(max(self.basePos[1] - panAmt, self.minPanY), self.maxPanY)
			self.base.setPosition(*self.basePos)
			self.prevMousePos = e.getPosition()


	def onEvent(self):
		e = getEvent()
		if e.getServiceType() == ServiceType.Controller:
			if e.getSourceId() == 1:
				# space navigator controls
				self.onSpaceNavEvent(e)
			elif e.getSourceId() == 0:
				self.onGameControllerEvent(e)
			return

		if self.allowStereoSetting:
			if e.isKeyDown(ord('x')):
				self.setStereo(not isStereoEnabled())

		self.onMouseEvent(e)

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

		self.angles = [
			self.angles[0] + pitch,
			self.angles[1] + yaw,
			self.angles[2] + roll
		]

		# clamping angles
		self.angles = [
			min(max(self.angles[0], -self.xClamp), self.xClamp),
			self.angles[1],
			min(max(self.angles[2], -self.zClamp), self.zClamp),
		]

		self.basePos = [
			self.basePos[0] + x,
			self.basePos[1] + y,
			self.basePos[2] + z,
		]

		camZ = getDefaultCamera().getPosition().z

		self.basePos = [
			min(max(self.basePos[0], 0.0), 0.0),
			min(max(self.basePos[1], self.minPanY), self.maxPanY),
			min(max(self.basePos[2], camZ - self.maxZoomDist), camZ - self.minZoomDist),
		]

		self.base.setPosition(Vector3(*self.basePos))
		self.base.translate(0, y, 0, Space.Local)
		self.base.setOrientation(self.initialRot * quaternionFromEulerDeg(*self.angles))

	# spin after idleTime seconds
	# TODO: sync this with self.angles
	def onUpdate(self, frame, time, dt):
		self.timeSinceEvent += dt
		self.doControllerMove()

		if self.timeSinceEvent >= (self.idleTime * 1.5):
			self.angles[1] += self.spinSpeed * dt
			self.base.setOrientation(self.initialRot * quaternionFromEulerDeg(*self.angles))
		# linearly speed up
		elif self.timeSinceEvent >= self.idleTime:
			d = self.timeSinceEvent - self.idleTime
			self.angles[1] += 2.0 * d / self.idleTime * self.spinSpeed * dt
			self.base.setOrientation(self.initialRot * quaternionFromEulerDeg(*self.angles))

	demoPanSpeed = 0.02
	demoMin = -0.45
	demoMax = .42

	progress = 0.0

	# spin after idleTime seconds
	def onUpdateDemo(self, frame, time, dt):
		self.timeSinceEvent += dt
		self.doControllerMove()

		if self.timeSinceEvent >= (self.idleTime * 1.5):
			self.angles[1] += self.spinSpeed * dt
			self.base.setOrientation(self.initialRot * quaternionFromEulerDeg(*self.angles))
			#sawtooth
			self.progess = self.demoMin + (self.demoMax - self.demoMin) * abs(((self.demoPanSpeed * 0.03 * time) % 2) - 1)
			#sine
			#self.progess = self.demoMin + (self.demoMax - self.demoMin) * (0.5 * (sin(self.demoPanSpeed * radians(time))+ 1.0))
			self.basePos[1] = self.progess
			self.base.setPosition(*self.basePos)

		# linearly speed up
		elif self.timeSinceEvent >= self.idleTime:
			d = self.timeSinceEvent - self.idleTime
			self.angles[1] += 2.0 * d / self.idleTime * self.spinSpeed * dt
			self.base.setOrientation(self.initialRot * quaternionFromEulerDeg(*self.angles))

	def onPressKey(self, direction):
		pass

	def setStereo(self, toggle):
		if toggle:
			#getDisplayConfig().stereoMode = StereoMode.LineInterleaved
			if not isStereoEnabled():
				toggleStereo()
			getDefaultCamera().setEyeSeparation(0.0007)

			print "Stereo On"
		else:
			if isStereoEnabled():
				toggleStereo()
			#getDisplayConfig().stereoMode = StereoMode.Mono
			getDefaultCamera().setEyeSeparation(0.06)
			print "Stereo Off"


if __name__ == "__main__":

	fileToLoad = "/local/examples/fashion/Mook_mix1_initial.fbx"

	objects = []

	getSceneManager().setBackgroundColor(Color(0,0,0,0))

	cam = getDefaultCamera()
	cam.setControllerEnabled(False)
	cam.setPosition(Vector3(0, 0, 3) - cam.getHeadOffset())
	cam.setNearFarZ(0.001, 50)
	cam.setEyeSeparation(0.0007)

	turntable = Turntable()
	turntable.allowStereoSetting = True
	turntable.loadModel(fileToLoad)

	setEventFunction(turntable.onEvent)
	setUpdateFunction(turntable.onUpdate)

	print "\n=========================\n"
	print " Use x key to toggle Stereo"
	print "\n=========================\n"
	print
	if isStereoEnabled():
		print "Stereo is ENABLED"
	else:
		print "Stereo is DISABLED"
	print
