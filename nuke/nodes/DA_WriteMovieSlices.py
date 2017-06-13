import nuke
import os

class DA_WriteMovieSlices:

    @staticmethod
    def onUserCreateCallback():
        """
        Populate defaults on creation of a DA_WriteMovieSlices node.
        """
        if (nuke.thisNode().Class().endswith('DA_WriteMovieSlices')):
            nuke.thisNode().knob('first').setValue(nuke.root().knob('first_frame').value())
            nuke.thisNode().knob('last').setValue(nuke.root().knob('last_frame').value())


    @staticmethod
    def beforeRenderCallback():
        """
        Prepare to render from a DA_WriteMovieSlices node.
        """
        slice_number = nuke.thisNode().knob('slice').value()
        output_fpath = nuke.thisParent().knob('file').value()

        if not len(output_fpath) > 0:
            raise RuntimeError('No output filepath has been specified!')

        base = os.path.basename(output_fpath)

        prefix = base[:base.index('.')]
        suffix = base[base.index('.'):]

        slice_name = 'slice_%s' % int(slice_number)

        destdir = os.path.join(os.path.dirname(output_fpath), prefix, slice_name)
        destfile = prefix + '_' + slice_name + suffix

        if not os.path.exists(destdir):
            os.makedirs(destdir)

        nuke.thisNode().knob('file').setValue(os.path.join(destdir, destfile))
        nuke.thisNode().knob('first').setValue(nuke.thisParent().knob('first').value())
        nuke.thisNode().knob('last').setValue(nuke.thisParent().knob('last').value())
