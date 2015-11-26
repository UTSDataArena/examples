# TODO: append GeoLoader package to python search path in omegalib: workaround
import sys
sys.path.append('/local/examples')

import glob
from omega import setEventFunction, setUpdateFunction
from GeoLoader.GeometryFile import GeometryFile
from GeoLoader.DAEventHandler import DAEventHandler

handler = DAEventHandler()
handler.initialCamPosition = [0, 0, 50]

geos = []
files = glob.glob("/da/proj/cranioFacialGenetics/out/*.obj")
for i in range(0, len(files)):
    geos.append(GeometryFile(files[i]))
    geos[i].model.setScale(0.1, 0.1, 0.1)
    handler.addGeo(geos[i])

handler.nextModel()

setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
