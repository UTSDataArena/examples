# TODO: append GeoLoader package to python search path in omegalib: workaround
import os.path, sys
basePath = os.path.dirname(os.path.abspath(__file__)) # for current dir of file
modulePath = os.path.dirname(basePath) # for GeoLoader packages - '/local/examples'
sys.path.append(modulePath) 

from omega import setEventFunction, setUpdateFunction
from pipelines.objects import Canvas
from pipelines.handler import CanvasHandler

width = 2680
height = 1720
distance = 0

fileprefix = "file://{}/".format(basePath)
files = [
    "CompetitiveGrantsIncome/Commonwealth",
    "CompetitiveGrantsIncome/NonCommonwealth",
#    "CompetitiveGrantsIncome/Total",
    #"CompetitiveGrantsIncome/RuralRD",
]

handler = CanvasHandler()
handler.setPosition([1.35, -0.75, 2.7])
for i in range(0,len(files)):
    canvas = Canvas(fileprefix + files[i] + "/index.html", width, height)
    handler.addCanvas(canvas)

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
