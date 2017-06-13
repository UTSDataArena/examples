import nuke

from nodes.DA_WriteMovieSlices import DA_WriteMovieSlices

## Custom DA formats

da_mono = '10080 1200 1 Data Arena Mono'
da_stereo = '10080 2400 1 Data Arena Stereo'
da_stereo_movie = '10320 2400 1 Data Arena Stereo Movie'

nuke.addFormat(da_mono)
nuke.addFormat(da_stereo)
nuke.addFormat(da_stereo_movie)

nuke.root()['format'].setValue('Data Arena Mono')
