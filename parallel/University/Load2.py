# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/home/fabian/Code/examples')

from omega import setEventFunction, setUpdateFunction
from GeoLoader.GeometryFile import Canvas
from GeoLoader.DAEventHandler import CanvasHandler

cam = getDefaultCamera()
cam.setControllerEnabled(False)

width = 2680
height = 1720
distance = 0

fileprefix = "file:///local/examples/parallel/University/"
fileprefix = "file:///home/fabian/Code/examples/parallel/University/"
files = [
    "CompetitiveGrantsIncome/Commonwealth",
    "CompetitiveGrantsIncome/NonCommonwealth",
#    "CompetitiveGrantsIncome/Total",
    #"CompetitiveGrantsIncome/RuralRD",
]


handler = CanvasHandler()
for i in range(0,len(files)):
    geo = Canvas(fileprefix + files[i] + "/index.html", width, height)
    handler.addGeo(geo)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
