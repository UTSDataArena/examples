Geometry Loader for the Data Arena
==================================

These Python scripts offer a modular way to display geometry data via omegalib.
Supported input formats are *.obj*, *.fbx* [list all available via cyclops]
The files are loaded as shown in `GeometryLoader.py`.

Navigation in the scene is possible with Mouse and Space Navigator (GameController comming soon).

The keyboard is used to configure the input devices and display the settings.
This can be done by pressing the *i* key (info).

First of all, there are two modes of navigation, either the object or the camera is moved and rotated.
To switch between these modes the *m* key is used.
In the following, all movement of the 'object' can also be applied to the camera in the other mode.

To restrict the navigation along axes the following keys are used:

	* x,y or z toggles the movement on axis x,y or z
	* p,j or r toggles the rotation on axis x,y or z (pitch, jam jar, roll)
									
Further, the *n* key resets the position of the object, respectively camera, to the start.
If the 3D stereo view is available this can be switched on or off with the *s* key.

**Note**
If the object is out of view and does not come back on a reset mind that you reset both, camera and object position.

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
