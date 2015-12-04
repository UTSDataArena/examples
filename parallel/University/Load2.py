# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

from omega import setEventFunction, setUpdateFunction
from pipelines.objects import Canvas
from pipelines.handler import CanvasHandler

width = 2680
height = 1720
distance = 0

fileprefix = "file:///local/examples/parallel/University/"
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
