# Exporting models to omegalib from Blender, Maya or 3ds Max

There are a few exporters from 3D modelling packages to osg/omegalib. 
Check http://trac.openscenegraph.org/projects/osg//wiki/Community/Plugins for available exporters, there are exporters for 3D Studio Max, Maya and Blender (plugins for other model packages might exist elsewhere). The best plugin for Blender is maintained under https://github.com/cedricpinson/osgexport, use this to export your scene into .osgt or .ive.

While there is a comprehensive documentation for the autodesk 3ds exporter at https://sourceforge.net/p/osgmaxexp/mediawiki/Documentation/, there is no documentation for osgexport.

Here are some best practices, which we have found to work well, generally:
build the materials in the standrad material editor (not the cycles/node one). UV textures should also be  set in the standard texture panel and not in the 3d view UV settings.


* Apply all modifiers before exporting (can be ticked as option in exporter)
* Only one texture per material, any other textures will probably be ignored
* Use only UV mapping, generated texture coordinates often do not function as expected
* Set textures as the diffuse color 
* Alpha textures do not work in the export in the current version
* Always set blender to use relative paths. The osgexporter will copy all textures to a subdirectory of your blender file.

#### Converting to a binary format

The exported .osgt format is a ascii text file, which contains the scenegraph in a very readible format. This is nice to look at, what kinds of objects will be created in osg and can be used to debug errors in imports. However, loading these files can take some time and they might not be in a very omptimized state. OSG provides the `osgconv` tool to convert from many formats (osgt, obj, fbx, ..) to .ive, the binary format for osg. When converting, there is a plethora of options, which can be supplied to optimize the scenegraph for osg (look at them with osgconv --help). 
Many options are not necessary for normal usage, but become useful if dealing with large datasets. One particulary neat option is to automatically compress all textures in opengl with a opengl or dxt compression format. This can reduce the size of the needed gpu texture memory by a factor of three. There are some restrictions on the size of textures with compressed textures, however. If you are experiencing segfault with


