from webView import *

#width = 3840
width = 11020
height = 1200
#width = 5760
#height = 600

ww = None

ui = UiModule.createAndInitialize()
uiroot = ui.getUi()

if(isMaster()):
	ww = WebView.create(width, height)
	ww.loadUrl("http://exposedata.com/parallel/")
	ww.setZoom(200)
	# neat webgl aquarium demo
	#ww.loadUrl("http://webglsamples.googlecode.com/hg/aquarium/aquarium.html")
	frame = WebFrame.create(uiroot)
	frame.setView(ww)
else:
	ww = PixelData.create(width, height, PixelFormat.FormatRgba)
	frame = Image.create(uiroot)
	frame.setDestRect(250,0,11020, 1200)
	frame.setData(ww)

ImageBroadcastModule.instance().addChannel(ww, "webpage", ImageFormat.None)
	
