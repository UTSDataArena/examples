# Mayavi
(todo insert cool pic of mayavi?)

[Mayavi](http://code.enthought.com/projects/mayavi/) is a scientific visualization tool to easily create 3D visualizations. It internally uses VTK (Visualization Toolkit) and therefore includes a large number of visualization metaphers which can be used. Mayavis advantage over other visualization tools is, that it understands and uses numpy for its computations, therefore it is easily integrated into the workflow of scientific computations which often use numpy and scipy.

#### Install yourself
The easiest way to install Mayavi yourself is to get it via the conda installer of the python Anaconda distribution. This will install a pre-packaged binary into the anaconda directory and is then automatically available on the python path. 

### Mayavi from source
If you want to build mayavi from source, you will need to also build VTK from source. Mayavi will work best with VTK 5.10, which is also built from source. There are some issues with the qt backend, however, this is still preferred over the wxwidgets backend as wxwidgets does not support all mayavi gui applications.

To run mayavi python scripts, you must either use the runMayavi.sh, found in  runscript with your python script as argument OR execute the steps in the script once yourself :  set the environment variables QT_API=pyqt and ETS_TOOLKIT=qt4 and put this in the top of your python script:
```python
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
```
This is a workaround to set python qt bindings for qt4 to a certain API version.

Please refer to the mayavi docs for documentation and also check out some of the examples in the mayavi folder. They will give you a good impression on whats possible with the tool.

