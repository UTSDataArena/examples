import nuke
import os

from nodes.DA_WriteMovieSlices import DA_WriteMovieSlices

gizmos = '%s/gizmos' % os.path.dirname(os.path.abspath(__file__))

toolbar = nuke.toolbar('Nodes')

da_menu = toolbar.addMenu('DataArena')
da_menu.addCommand('DA_WriteMovieSlices', 'nuke.createNode("%s/DA_WriteMovieSlices")' % gizmos)

nuke.addOnUserCreate(DA_WriteMovieSlices.onUserCreateCallback)
