from math import *
from euclid import *
from omega import *
from omegaToolkit import *
from cyclops import *

flags = [
	EventFlags.SpecialButton1,
	EventFlags.SpecialButton2,
	EventFlags.SpecialButton3,
	EventFlags.Button1,
	EventFlags.Button2,
	EventFlags.Button3,
	EventFlags.Button4,
	EventFlags.Button5,
	EventFlags.Button6,
	EventFlags.Button7,
	EventFlags.ButtonUp,
	EventFlags.ButtonDown,
	EventFlags.ButtonLeft,
	EventFlags.ButtonRight,
]

obj = None
altObj = None


initPos = Vector3(0, 2, -5)
initRot = quaternionFromEulerDeg(30, 30, 30)

rotOffset = quaternionFromEulerDeg(0,0,0)

rotSensitivity = 2.0
transSensitivity = 0.1

scaleRot_JarLid    = 1.0
scaleRot_Motorbike = 0.7
scaleRot_Doorknob  = 0.2

selfRighting = False
selfRightingDelay = 0.5
selfRightingSpeed = 1.0

startRighting = False

pivotOffset = None

timeSinceMove = 0

rot = None
eul = None
destRot = None

myDt = 0

# fetched from python euclid issue page
# https://code.google.com/p/pyeuclid/issues/detail?id=18
# bug in the new_interpolate implementation?
def my_new_interpolate(q1, q2, t):
    assert isinstance(q1, Quaternion) and isinstance(q2, Quaternion)
    Q = Quaternion.new_identity()

    costheta = q1.w * q2.w + q1.x * q2.x + q1.y * q2.y + q1.z * q2.z
    if costheta < -1.0:
		costheta = -1.0

    if costheta < 0.:
        costheta = -costheta
        q1 = q1.conjugated()
    elif costheta > 1:
        costheta = 1
    elif costheta == 1.0:
    #elif abs(costheta - 1.0) < 0.01:
        Q.w = q1.w
        Q.x = q1.x
        Q.y = q1.y
        Q.z = q1.z
        return Q
    theta = math.acos(costheta)
    sintheta = math.sqrt(1.0 - costheta * costheta)
    try:
        ratio1 = math.sin((1 - t) * theta) / sintheta
    except ZeroDivisionError:
        Q.w = q1.w
        Q.x = q1.x
        Q.y = q1.y
        Q.z = q1.z
        return Q
    ratio2 = math.sin(t * theta) / sintheta

    Q.w = q1.w * ratio1 + q2.w * ratio2
    Q.x = q1.x * ratio1 + q2.x * ratio2
    Q.y = q1.y * ratio1 + q2.y * ratio2
    Q.z = q1.z * ratio1 + q2.z * ratio2
    return Q

middleMouseDown = False
rightMouseDown = False
leftMouseDown = False

def onUpdate(frame, time, dt):
	global timeSinceMove
	global selfRighting, selfRightingDelay, selfRightingSpeed
	global initRot, rotOffset, obj
	global rot, eul, myDt, destRot
	global startRighting
	global middleMouseDown
	global rightMouseDown
	global leftMouseDown


	timeSinceMove += dt

	#if selfRighting:
		#if startRighting:
			#myDt += dt
			#n = myDt / selfRightingSpeed
			#eul = rot.get_euler()

			#if n > 1.0:
				#n = 1.0
				#startRighting = False
				#print time, "Stop righting to", Quaternion.new_rotate_euler(eul[0],0, eul[2]).get_euler()
				##print time, "Stop righting to", quaternionFromEuler(eul[2],eul[0], 0).get_euler()
			## obj.setOrientation(Quaternion.new_interpolate(rot, initRot, selfRightingSpeed * dt))
			## quaternionFromEuler(eul[2], eul[0], eul[1])
			## this effectively resets z axis orientation ie doorknob)
			## seems to be bug with new_interpolate, gives different values depending on how its called??
			##obj.setOrientation(Quaternion.new_interpolate(rot, quaternionFromEuler(eul[2],eul[0], 0), n * n))
			##print n*n, Quaternion.new_interpolate(rot, quaternionFromEuler(eul[2],eul[0], 0), n * n).get_euler()
			#obj.setOrientation(Quaternion.new_interpolate(rot, Quaternion.new_rotate_euler(eul[0],0, eul[2]), n * n))
			#print n*n, Quaternion.new_interpolate(rot, Quaternion.new_rotate_euler(eul[0],0, eul[2]), n * n).get_euler()

		#elif timeSinceMove > selfRightingDelay and timeSinceMove <= selfRightingDelay + selfRightingSpeed:
			##rot = obj.getOrientation()
			## change rotation to account for buggy sign?
			##rot = quaternionFromEuler(eul[2], -eul[0], eul[1])
			##rot.x = -rot.x # this isnt right.. fixes some parts, makes other parts worse
			##eul = rot.get_euler()
			#myDt = 0
			#startRighting = True
			#eul = rot.get_euler()
			#print time, "start righting from", eul
	if selfRighting:
		if not (rot and eul and destRot):
			return
		if timeSinceMove > selfRightingDelay and timeSinceMove <= selfRightingDelay + selfRightingSpeed:
			myDt += dt
			n = myDt / selfRightingSpeed
			#rot = obj.getOrientation()
			#eul = rot.get_euler()
			#if eul[0] > 0 and eul[1] < 0 and eul[2] > 0:
				#eul = (-eul[0], eul[1], -eul[2])

			#elif eul[0] > 0 and eul[1] > 0 and eul[2] < 0:
				#eul = (-eul[0], -eul[1], eul[2])

			#elif eul[0] < 0 and eul[1] > 0 and eul[2] > 0:
				#eul = (-eul[0], eul[1], eul[2])

			if n > 1.0:
				n = 1.0
				#print time, "Stop righting to", Quaternion.new_rotate_euler(eul[0],0, eul[2]).get_euler()
				#print time, "Stop righting to", quaternionFromEuler(eul[2],eul[0], 0).get_euler()
			# obj.setOrientation(Quaternion.new_interpolate(rot, initRot, selfRightingSpeed * dt))
			# quaternionFromEuler(eul[2], eul[0], eul[1])
			# this effectively resets z axis orientation ie doorknob)
			# seems to be bug with new_interpolate, gives different values depending on how its called??
			#obj.setOrientation(Quaternion.new_interpolate(rot, quaternionFromEuler(eul[2],eul[0], 0), n * n))
			#print n*n, Quaternion.new_interpolate(rot, quaternionFromEuler(eul[2],eul[0], 0), n * n).get_euler()
			#newQuat = Quaternion.new_interpolate(rot, destRot, n * n)
			newQuat = my_new_interpolate(rot, destRot, n * n)
			obj.setOrientation(newQuat)
			#obj.setOrientation(Quaternion.new_interpolate(rot, Quaternion.new_rotate_euler(eul[0],0, eul[2]), n * n))
			#print '%.2f' % (n*n), ['%.2f' % a for a in newQuat.get_euler()],
			#print ['%.2f' % a for a in rot.get_euler()], ['%.2f' % a for a in destRot.get_euler()]
		else:
			#rot = obj.getOrientation()
			#eul = rot.get_euler()
			myDt = 0

	if middleMouseDown:
		cam = getDefaultCamera()
		cam.translate(Vector3(0,0,-1.0 * dt), Space.Local)

	if rightMouseDown:
		cam = getDefaultCamera()
		if leftMouseDown:
			cam.translate(Vector3(0,0.2 * dt, 0), Space.Local)
		else:
			cam.translate(Vector3(0,-0.2 * dt, 0), Space.Local)



def reset():
	global obj, initPos, initRot, rotOffset
	obj.setPosition(initPos)
	obj.setOrientation(initRot)
	obj.rotate(rotOffset, Space.Local)

def onEvent():
	global flags, initRot, rotSensitivity, transSensitivity, initPos, obj, rotOffset
        global scaleRot_JarLid, scaleRot_Motorbike, scaleRot_Doorknob
	global timeSinceMove
	global startRighting
	global pivotOffset
	global middleMouseDown
	global rightMouseDown
	global leftMouseDown

	global rot, eul, destRot

	e = getEvent()
	startRighting = False

	# Space Navigator axes:
	#0 (-left, +right)
	#1 (-forward, +back)
	#2 (-up, +down)
	#3 pitch (-forward, +back)
	#4 roll (-right, +left)
	#5 yaw (-left, +right)

	# Differentiate controller by source id.. may change this to something else (userId?),
	# as sourceId is also used for key
	if e.getServiceType() == ServiceType.Controller and e.getSourceId() == 1:
		# Move in x, y and z
		x = e.getExtraDataFloat(0) * transSensitivity
		y = -e.getExtraDataFloat(2) * transSensitivity # * 0.2
		z = e.getExtraDataFloat(1) * transSensitivity

		# Rotate like a motorbike handle
		pitch = e.getExtraDataFloat(3) * rotSensitivity * scaleRot_Motorbike
		# Rotate like a jar lid
		yaw = -e.getExtraDataFloat(5) * rotSensitivity * scaleRot_JarLid
		# Rotate like a doorknob
		roll = e.getExtraDataFloat(4) * rotSensitivity * scaleRot_Doorknob # reduce sensitivity this way
		#roll = 0

		# Set the values
		obj.translate(x,y,z, Space.Local)
		#obj.translate(x,z,y, Space.Local)
		#obj.getChildByIndex(0).rotate(quaternionFromEulerDeg(pitch, yaw, roll), Space.Local)
		if pivotOffset:
			obj.translate(-pivotOffset, Space.Local)
		obj.rotate(quaternionFromEulerDeg(pitch, yaw, roll), Space.Local)
		if pivotOffset:
			obj.translate(pivotOffset, Space.Local)

		#obj.rotate(quaternionFromEulerDeg(pitch, roll, yaw), Space.Local)

		# TODO: rotate object should be in camera space, esp. roll

		#obj.setOrientation(initRot * quaternionFromEulerDeg(0, rot, 0))
		#for i in range(e.getExtraDataItems()):
			#print e.getExtraDataFloat(i)

		# Space Navigator buttons:
		# 0 - left button
		# 1 - right button
		if e.isButtonDown(EventFlags.Button1):
			reset()

		#if e.isButtonDown(EventFlags.Button2):
			#pass

		rot = obj.getOrientation()
		eul = rot.get_euler()
		destRot = Quaternion.new_rotate_euler(eul[0], 0, eul[2])
		#print "current pos:", ['%.2f' % a for a in rot.get_euler()], ['%.2f' % a for a in destRot.get_euler()]
		#print "quaternions:", rot, destRot
		timeSinceMove = 0
		myDt = 0

	if e.isButtonDown(EventFlags.Left):
		leftMouseDown = True
	elif e.isButtonUp(EventFlags.Left):
		leftMouseDown = False

	if e.isButtonDown(EventFlags.Middle):
		middleMouseDown = True
	elif e.isButtonUp(EventFlags.Middle):
		middleMouseDown = False

	if e.isButtonDown(EventFlags.Right):
		rightMouseDown = True
	elif e.isButtonUp(EventFlags.Right):
		rightMouseDown = False

	# ps3/4 controllers
	# Left analog:
	# channel 0: left/right
	# channel 1: up/down
	# Right analog:
	# channel 2: left/right
	# channel 3: up/down
	if e.getServiceType() == ServiceType.Controller and e.getSourceId() == 0:
		# Move in x, y and z
		#x = e.getExtraDataFloat(0) * transSensitivity
		#y = -e.getExtraDataFloat(2) * transSensitivity # * 0.2
		#z = e.getExtraDataFloat(1) * transSensitivity
		x = e.getExtraDataFloat(2) * transSensitivity
		y = 0
		z = e.getExtraDataFloat(3) * transSensitivity

		## Rotate like a motorbike handle
		#pitch = e.getExtraDataFloat(3) * rotSensitivity * 0.7
		## Rotate like a jar lid
		#yaw = -e.getExtraDataFloat(5) * rotSensitivity
		## Rotate like a doorknob
		#roll = e.getExtraDataFloat(4) * rotSensitivity * 0.2 # reduce sensitivity this way
		##roll = 0
		# Rotate like a motorbike handle
		pitch = e.getExtraDataFloat(1) * rotSensitivity * 1.0
		# Rotate like a jar lid
		yaw = -e.getExtraDataFloat(0) * rotSensitivity * 1.0
		# Rotate like a doorknob
		roll = 0

		# Set the values
		obj.translate(x,y,z, Space.Local)
		#obj.translate(x,z,y, Space.Local)
		#obj.getChildByIndex(0).rotate(quaternionFromEulerDeg(pitch, yaw, roll), Space.Local)
		if pivotOffset:
			obj.translate(-pivotOffset, Space.Local)
		obj.rotate(quaternionFromEulerDeg(pitch, yaw, roll), Space.Local)
		if pivotOffset:
			obj.translate(pivotOffset, Space.Local)
		#obj.rotate(quaternionFromEulerDeg(pitch, roll, yaw), Space.Local)

		# TODO: rotate object should be in camera space, esp. roll

		#obj.setOrientation(initRot * quaternionFromEulerDeg(0, rot, 0))
		#for i in range(e.getExtraDataItems()):
			#print e.getExtraDataFloat(i)

		# Space Navigator buttons:
		# 0 - left button
		# 1 - right button
		if e.isButtonDown(EventFlags.Button1):
			reset()

		#if e.isButtonDown(EventFlags.Button2):
			#pass

		rot = obj.getOrientation()
		eul = rot.get_euler()
		destRot = Quaternion.new_rotate_euler(eul[0], 0, eul[2])
		#print "current pos:", ['%.2f' % a for a in rot.get_euler()], ['%.2f' % a for a in destRot.get_euler()]
		#print "quaternions:", rot, destRot
		timeSinceMove = 0
		myDt = 0

	# toggle between camera and object-based controls
	if e.isKeyUp(ord('z')) or e.isKeyUp(ord('Z')):
		if obj and altObj:
			obj, altObj = altObj, obj

	for i in flags:
		if e.isButtonDown(i):
			print "Button", i, "is down"
		elif e.isButtonUp(i):
			print "Button", i, "is up"
