// Processing in the Data Arena
// 3D Object Mode Sketches Template
// with VRPN connection support

// This example uses the 3D Connexion Space Navigator
// to control rotations.

import peasy.*;
import vrpn.*;

PeasyCam cam;
DeviceRead read;

// If you're in the Data Arena, set this to true
// and run matrix.solo.mono in a shell
boolean dataArena = false;

float camRotateX, camRotateY, camRotateZ;
float dist = 800;

void settings() {
  if (dataArena) {
    // size will be detected automagically
    size(displayWidth, 1200, P3D);
  } else {
    // set your custom testing resolution here
    size(1920, 1200, P3D);
  }
}

void setup() {
  cam = new PeasyCam(this, 800);
  
  read = new DeviceRead();
  read.vrpnSetup();
}

void draw() {
  updateCam();
  background(0);
  fill(0);
  stroke(0, 255, 0);
  rotateY(radians(25));
  rotateX(radians(15));
  sphere(200);
}

void updateCam() {
  dist += (read.spty*50);
  camRotateY = read.sprz*0.05;
  camRotateX = -read.sprx*0.05;
  camRotateZ = read.spry*0.05;
  cam.rotateY(camRotateY);
  cam.rotateX(camRotateX);
  cam.rotateZ(camRotateZ);
  cam.setDistance(dist, 1);
}