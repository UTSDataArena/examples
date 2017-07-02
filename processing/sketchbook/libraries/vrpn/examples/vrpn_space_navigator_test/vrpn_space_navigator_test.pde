// Using the VRPN library
// to read from a 3D Connexion Space Navigator

// Note: VRPN server must be running
// https://github.com/vrpn/vrpn/wiki

// This VRPN library was built from the master VRPN source
// Java files, and set up to run in Processing

// SpaceNavigator translation and rotation values
// are channeled into 6 variables
// each with a range of -0.875 to 0.875
// sptx : X translation value
// spty : Y translation value
// sptz : Z translation value
// sprx : X rotation value
// spry : Y rotation value
// sprz : Z rotation value
// And buttons into 2 booleans
// button1 : returns true if button 1 is pressed
// button2 : returns true if button 2 is pressed

// import the VRPN library
import vrpn.*;

// Create a new object from the Device Read class
DeviceRead read;

void setup() {
  size(500, 240);
  rectMode(CENTER);
  // initialise the object and setupVRPN (see other tab for more detail)
  read = new DeviceRead();
  read.vrpnSetup();
}

void draw() {
  background(0);

  fill(255);
  noStroke();
  text("device: " + read.deviceName, 30, 20);
  text("tx: " + read.sptx, 30, 50);
  text("ty: " + read.spty, 30, 70);
  text("tz: " + read.sptz, 30, 90);
  text("rx: " + read.sprx, 30, 110);
  text("ry: " + read.spry, 30, 130);
  text("rz: " + read.sprz, 30, 150);
  text("button1: " + "", 30, 170);
  text("button2: " + "", 30, 190);

  stroke(255);
  line(width/2, 47, width-30, 47);
  line(width/2, 67, width-30, 67);
  line(width/2, 87, width-30, 87);
  line(width/2, 107, width-30, 107);
  line(width/2, 127, width-30, 127);
  line(width/2, 147, width-30, 147);

  stroke(0);
  ellipse(map(read.sptx, -0.875, 0.875, width/2, width-30), 47, 7, 7);
  ellipse(map(read.spty, -0.875, 0.875, width/2, width-30), 67, 7, 7);
  ellipse(map(read.sptz, -0.875, 0.875, width/2, width-30), 87, 7, 7);
  ellipse(map(read.sprx, -0.875, 0.875, width/2, width-30), 107, 7, 7);
  ellipse(map(read.spry, -0.875, 0.875, width/2, width-30), 127, 7, 7);
  ellipse(map(read.sprz, -0.875, 0.875, width/2, width-30), 147, 7, 7);

  if (read.button1) {
    rect(map(0, -1, 1, width/2, width-30), 167, 9, 9);
  }

  if (read.button2) {
    rect(map(0, -1, 1, width/2, width-30), 187, 9, 9);
  }

  noFill();
  stroke(255);
  rect(map(0, -1, 1, width/2, width-30), 167, 11, 11);
  rect(map(0, -1, 1, width/2, width-30), 187, 11, 11);
}