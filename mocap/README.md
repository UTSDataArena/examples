# Examples for Motion Capture data

This Houdini project allows the interactive visualization of motion tracker data. Input data is provided in the /data directory in form of tabulator-separated channel files.
The Houdini .hipnc file contains three objects which can be used as a guiding example.
An introduction and documentation of the Houdini framework can be found [here](http://www.sidefx.com/docs/houdini15.0/basics/).

* `floor` optional ground surface
* `mocap` and `mocap1` example motion captures

### Structure of mocap

Input parameters of the object are:
* Mocap file
* Start line of data
* End line of data

The file name is used inside the `chopnet` node where the data is loaded and parsed into Houdini. This includes trimming the selected lines, removing the first column (frame number) and renaming the columns into attributes.
The nodes `box` and `trail` deliver the basic geometry which is copied to coordinates coming from the channel data. Finally, the coloring can be changed and the resulting geometry is merged into one output operator.
