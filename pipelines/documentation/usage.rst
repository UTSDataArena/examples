Usage
=====

This Python package offers a modular way to display visualizations in the Data Arena.
Classes in the `objects` module contain a visualization of data.
New visualizations should inherit the `BaseObject` or any existing type of data which is similar.
Available are:

* Geometry: Supported input formats are *.obj*, *.fbx*, *.ply* and displays the 3D model.
* OTL: Loads an Houdini OTL and instanciates the geometry.

The `handler` module provides the interaction with a visualization.
New handler should inherit from the `BaseHandler` or any similar existing handler.
Available are:

* GeometryHandler
* OTLHandler

Navigation
----------

Navigation in the scene is possible with Mouse and Space Navigator.

The keyboard is used to configure the input devices and display the settings.
This can be done by pressing the *i* key (info).

First of all, there are two modes of navigation, either the object or the camera is moved and rotated.
To switch between these modes the *m* key is used.
In the following, all movement of the 'object' can also be applied to the camera in the other mode.

To restrict the navigation along axes the following keys are used:

* x,y or z toggles the movement on axis x,y or z
* p,j or r toggles the rotation on axis x,y or z (pitch, jam jar, roll)
									
Further, the *n* key resets the position of the object, respectively camera, to the start.
This will not reset movement restrictions on axes!

**Note**
	If the object is out of view and does not come back on a reset mind that you reset both, camera and object position.

If the 3D stereo view is available this can be switched on or off with the *s* key.

Mouse
-----

The *Left Button* is used to move the object along the X and Y axis.
The *Right Button* is used to rotate the object:

* Moving the Mouse left and right will rotate the object along the Y axis, which turns the object to left or right.
* Moving the Mouse up and down will rotate the object along the X axis, which turns the object up and down.

The *Middle Button* is used to move the object along the Z axis (moving the mouse up and down) or rotation on the Z axis (clock-/anticlockwise).

Space Navigator
---------------

The six degrees of the Space Navigator are used to move or rotate the object.
Pushing the knob horizontally left or right moves the object on the X axis, forward and backward on the Z axis.
Pulling up or pushing down moves the obect on the Y axis.

To rotate the object on the Z or X axis the knob is pushed diagonally on the top corner either left/right or forward/backward.
Twisting the knob results in rotation along the Y axis.

The left button is used to reset the view to the default.
The right button toggles between the movement of the object or the camera.

Inverting Axes
--------------

If you prefer the object to move in the opposite direction when you use the input device, you can invert the axes by pressing *Ctrl* and the character of the axis.
This will result in different navigation behaviour, keep in mind in which mode you are!
This settings are not reset with *n*, but can be toggled all the time.

Developer Settings
------------------

The handler object has several parameters, which further tune the behaviour.
`__init__` contains the following parameters:

* Sensitivity tuning of Mouse and Space Navigator
* Preconfigured settings for axes restriction
* Preconfigured settings for axes inversion

  since the Space Navigator and Mouse send different values these settings are also adjusted in `onSpaceNavEvent()`

`Geometry.py` encapsulates the geometric data of a single object.
Likewise, `__init__` contains several parameters:

* Restrictions for maximum movement and rotation

  xAngClamp sets the maximum absolute rotation from the initial value
  
  xPosClamp sets the maximum absolute translation from the initial value
* textured can be activated, otherwise the color is set in `loadModel()`
* The initial position is at the origin if not changed
* As pivot point for object rotation we use the center of the bounding box as default

TODO: The implementation of the GameControler is not finished.
