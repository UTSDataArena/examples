from webView import *
from math import *
from cyclops import *

#width = 2048
#height = 1000

#width = 4096
width = 2648
#width = 3870
height = 900


cam = getDefaultCamera()
cam.setEyeSeparation(0)

ww = None

ui = UiModule.createAndInitialize()
uiroot = ui.getUi()

cont = Container.create(ContainerLayout.LayoutFree, ui.getUi())

screenCont = Container.create(ContainerLayout.LayoutFree, ui.getUi())
screenCont2 = Container.create(ContainerLayout.LayoutFree, ui.getUi())

myNode = SceneNode.create("myNode")

c3d = cont.get3dSettings()
c3d.enable3d = True
#c3d.position = Vector3(-6, 2.5, -2)
#c3d.position = Vector3(0, 2.5, -2) # orig
c3d.position = Vector3(0.04, 2.5, -2)
#c3d.position = Vector3(0, 2.5, -2.5)
c3d.scale = 0.001
c3d.node = myNode

c3d2 = screenCont.get3dSettings()
c3d2.enable3d = True
#c3d.position = Vector3(-6, 2.5, -2)
#c3d2.position = Vector3(-1.94, 2.5, -2) # orig
c3d2.position = Vector3(-1.98, 2.5, -2)
#c3d.position = Vector3(0, 2.5, -2.5)
c3d2.scale = 0.001
c3d2.node = myNode

c3d3 = screenCont2.get3dSettings()
c3d3.enable3d = True
#c3d.position = Vector3(-6, 2.5, -2)
#c3d2.position = Vector3(-1.94, 2.5, -2) # orig
c3d3.position = Vector3(2.8, 2.5, -2)
#c3d.position = Vector3(0, 2.5, -2.5)
c3d3.scale = 0.001
c3d3.node = myNode

screenshot = Image.create(screenCont)
screenshotImg = loadImage('/da/proj/parallelCoords/parallelCoords.affymetrix.png')

screenshot.setData(screenshotImg)
screenshot.setSourceRect(0,0, 1920, 1200)
screenshot.setDestRect(0,0, 1932, 1212)

screenshot2 = Image.create(screenCont2)

screenshot2.setData(screenshotImg)
screenshot2.setSourceRect(0,0, 1920, 1200)
screenshot2.setDestRect(0,0, 1932, 1212)

if(isMaster()):
	ww = WebView.create(width, height)
	#ww.setZoom(200)
	ww.loadUrl("http://exposedata.com/parallel/")
	#ww.loadUrl("file:///da/proj/parallelCoords/ParallelCoordinates/NutrientContents-ParallelCoordinates.htm")
	#ww.loadUrl("file:///da/proj/parallelCoords/merged/merged.htm")
	# neat webgl aquarium demo
	##ww.loadUrl("http://webglsamples.googlecode.com/hg/aquarium/aquarium.html")
	#frame = WebFrame.create(uiroot)
	frame = WebFrame.create(cont)
	frame.setView(ww)
else:
	#ww = PixelData.create(width, height, PixelFormat.FormatRgb) # rgb for jpeg
	ww = PixelData.create(width, height, PixelFormat.FormatRgba) # rgba for png and no compression
	frame = Image.create(cont)
	frame.setDestRect(0, 0, width + 12, height + 12)
	frame.setData(ww)

#ImageBroadcastModule.instance().addChannel(ww, "webpage", ImageFormat.FormatJpeg)
#ImageBroadcastModule.instance().addChannel(ww, "webpage", ImageFormat.FormatPng)
ImageBroadcastModule.instance().addChannel(ww, "webpage", ImageFormat.FormatNone)

cursorImg = loadImage('/da/sw/omegalib/myCursor.png')
cursorClickImg = loadImage('/da/sw/omegalib/myCursor_click.png')
currentUser = 0

cursors = []
labels = []

names = [
	"Glenn", # name of person controlling
	"Darren",
	"Ben",
	"Marcus",
	"Hugh",
]
cols = [
	'#FF0000',
	'#00FF00',
	'#0000FF',
	'#FFFF00',
	'#00FFFF',
]

for i in range(5):
	cursor = Image.create(cont)
	label = Label.create(cont)
	label.setText(names[i])
	label.setFont('fonts/arial.ttf 18')
	label.setColor(Color('white'))
	label.setPosition(Vector2(32, 12))
	label.setFillEnabled(True)
	label.setFillColor(Color(cols[i]))

	if i == 0:
		cursor.setSize(Vector2(32, 32))
		cursor.setData(cursorImg)
	else:
		cursor.setData(loadImage('/da/sw/omegalib/myCursor_' + str(i + 1) + '.png'))
		cursor.setSize(Vector2(24, 24))
	cursors.append(cursor)
	labels.append(label)

screen = getDisplayPixelSize()

prevOrientations = [[Quaternion()]] * len(names)
#prevOrientations = [Quaternion()] * len(names)

prevDiffAmt = 0.0

def diff(q1, q2):
	return ((abs(q2.w) + abs(q2.x) + abs(q2.y) + abs(q2.z)) -
		 (abs(q1.w) + abs(q1.x) + abs(q1.y) + abs(q1.z)))

def onEvent():

	global currentUser, cursors, labels
	global cursorClickImg, cursorImg
	global prevOrientations, prevDiffAmt

	e = getEvent()

	if e.getServiceType() == ServiceType.Mocap:
		if e.getExtraDataItems() >= 2:
			point = Vector2(e.getExtraDataInt(0), e.getExtraDataInt(1))
			if e.getUserId() > len(cursors):
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
				cursors[e.getUserId() - 1].setPosition(point)
				labels[e.getUserId() - 1].setPosition(point + Vector2(32, 12))

			prevDiffAmt = diffAmt

			prevOrientations[e.getUserId() - 1].append(e.getOrientation())
			if len(prevOrientations[e.getUserId() - 1]) >= 4:
				prevOrientations[e.getUserId() - 1].pop(0)

		if (e.getUserId() == 1):
			vec = e.getOrientation() * Vector3(0, 1, 0)

			if vec[1] < -0.6:
				cursors[e.getUserId() - 1].setData(cursorClickImg)
			else:
				cursors[e.getUserId() - 1].setData(cursorImg)


setEventFunction(onEvent)

# Getting rough time per frame
#def onUpdate(frame, time, dt):
	#if (isMaster()):
		#print time

#setUpdateFunction(onUpdate)
