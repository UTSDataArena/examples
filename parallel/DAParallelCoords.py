from webView import *

#width = 11020
#height = 1200
width = 1200
height = 800

ww = None

ui = UiModule.createAndInitialize()
uiroot = ui.getUi()

if(isMaster()):
	ww = WebView.create(width, height)
	ww.loadUrl("http://www.exposedata.com/parallel/")
	#ww.loadUrl("file://gene/index.htm")
	#ww.setZoom(200)
	frame = WebFrame.create(uiroot)
	frame.setView(ww)
else:
	ww = PixelData.create(width, height, PixelFormat.FormatRgba)
	frame = Image.create(uiroot)
	frame.setDestRect(250,0,11020, 1200)
	frame.setData(ww)

ImageBroadcastModule.instance().addChannel(ww, "webpage", ImageFormat.FormatNone)
