from webView import *
import os.path, sys
basePath = os.path.dirname(os.path.abspath(__file__)) # for current dir of file
modulePath = os.path.dirname(basePath) # for GeoLoader packages - '/local/examples'
sys.path.append(modulePath) 

#width = 11020
#height = 1200
width = 1200
height = 800

ww = None

ui = UiModule.createAndInitialize()
uiroot = ui.getUi()

if(isMaster()):
	ww = WebView.create(width, height)
	# ww.loadUrl("http://www.exposedata.com/parallel/") # original site
	ww.loadUrl("file://{}/food/NutrientDatabase.html".format(basePath))
	#ww.setZoom(200)
	frame = WebFrame.create(uiroot)
	frame.setView(ww)
else:
	ww = PixelData.create(width, height, PixelFormat.FormatRgba)
	frame = Image.create(uiroot)
	frame.setDestRect(250,0,11020, 1200)
	frame.setData(ww)

ImageBroadcastModule.instance().addChannel(ww, "webpage", ImageFormat.FormatNone)
