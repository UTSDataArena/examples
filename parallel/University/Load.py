from webView import WebView, WebFrame
from euclid import Vector2, Vector3
from omega import SceneNode, getDefaultCamera, getEvent, ServiceType, ImageFormat, Color, isMaster, PixelData
from omegaToolkit import ImageBroadcastModule, Container, ContainerLayout, Label, Image

width = 1280
height = 1720
distance = 20

cam = getDefaultCamera()
cam.setEyeSeparation(0)

fileprefix = "file:///local/examples/parallel/University/"
files = [
    "CompetitiveGrantsIncome/Commonwealth",
    "CompetitiveGrantsIncome/Total",
    "CompetitiveGrantsIncome/NonCommonwealth",
]

myNode = SceneNode.create("myNode")
ui = UiModule.createAndInitialize()

cont = Container.create(ContainerLayout.LayoutFree, ui.getUi())
cont.setWidth(len(files)*(width+distance))
cont.setHeight(height)
c3d = cont.get3dSettings()
c3d.enable3d = True
c3d.position = Vector3(-2.3, 2.5, -5)
c3d.scale = 0.001
c3d.node = myNode

views = []
frames = []


for i in range(0,len(files)):
    if isMaster():
        views.append(WebView.create(width, height))
        views[i].loadUrl(fileprefix + files[i] + "/index.html")
        frames.append(WebFrame.create(cont))
        frames[i].setView(views[i])
    else:
        views.append(PixelData.create(width, height, PixelFormat.FormatRgba))
	frames.append(Image.create(cont))
	#frame[i].setDestRect(0, 0, width + 12, height + 12)
	frame[i].setDestRect(0, 0, width, height)
	frame[i].setData(views[i])
    frames[i].setPosition(Vector2(i*(width+distance), 0))
    ImageBroadcastModule.instance().addChannel(views[i], "webpage" + str(i), ImageFormat.FormatNone)

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

prevOrientations = [[Quaternion()]] * len(names)

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
