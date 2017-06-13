// Processing in the Data Arena
// 3D Scene Mode Sketches Template
// with VRPN connection support

// This example uses the 3D Connexion Space Navigator
// to control camera tranformation and rotation.

import peasy.*;
import vrpn.*;

DeviceRead read;
PeasyCam cam;

// If you're in the Data Arena, set this to true
// and run matrix.solo.mono in a shell
boolean dataArena = false;

// Camera
float[] getCamRotation, getCamPosition, getCamTarget;
PVector camDirection, camPosition, camTarget;
float camTranslateX, camTranslateY, camTranslateZ, camTranslateXLerp, camTranslateYLerp, camTranslateZLerp;
float camRotateX, camRotateY, camRotateZ, camRotateXLerp, camRotateYLerp, camRotateZLerp;
float lerpSpeed = 0.1;
float tranSen = 10;
float rotSen = 0.8;

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
  cam = new PeasyCam(this, 0, 0, 5000, 10);
  cam.setMinimumDistance(10);
  cam.setMaximumDistance(10);
  camDirection = new PVector();
  camPosition = new PVector();
  camTarget = new PVector();

  read = new DeviceRead();
  read.vrpnSetup();
}

void draw() {
  // Remember to run camUpdate in draw to refresh camera position
  updateCam();

  // Also, use the perspective() function to adjust your field of fiew
  // and the far clipping plane
  // You might want to test various FOV values in the Data Arena
  perspective(PI/3.0, (float)width / (float)height, 10, 100000);

  background(0);
  stroke(0);
  strokeWeight(1);
  for (int i = -2000; i < 2000; i += 100) {
    for (int j = -2000; j < 2000; j += 100) {
      pushMatrix();
      translate(i, j, 0);
      fill(0);
      stroke(0, 255, 0);
      box(50);
      popMatrix();
    }
  }

  printCamDetail();
}


// the updateCam() function manages all PeasyCam functions
// and calculates the vector for forward motion
void updateCam() {
  getCamPosition = cam.getLookAt();
  camPosition.x = getCamPosition[0];
  camPosition.y = getCamPosition[1];
  camPosition.z = getCamPosition[2];
  getCamTarget = cam.getPosition();
  camTarget.x = getCamTarget[0];
  camTarget.y = getCamTarget[1];
  camTarget.z = getCamTarget[2];

  camTranslateX = read.sptx*tranSen;
  camTranslateY = read.sptz*tranSen;
  camTranslateZ = -read.spty*(tranSen*3);
  camRotateX = -read.sprx*rotSen;
  camRotateY = -read.sprz*rotSen;
  camRotateZ = -read.spry*(rotSen/2);

  camDirection = PVector.sub(camPosition, camTarget);
  camDirection.normalize();
  camDirection.mult((camTranslateZ));
  camPosition.add(camDirection);
  cam.lookAt(camPosition.x, camPosition.y, camPosition.z, 0);
  cam.pan(camTranslateX, camTranslateY);

  cam.rotateX(radians(camRotateX));
  cam.rotateY(radians(camRotateY));
  cam.rotateZ(radians(camRotateZ));
}

// this function demonstrates displaying on-screen graphics
// or a heads-up display
void printCamDetail() {
  float[] getCamRotation = cam.getRotations();
  cam.beginHUD();
  textSize(12);
  fill(255);
  text("Frames per second: " + (int)frameRate, 20, 20);
  text("Camera rotations: ", 20, 50);
  text("x: " + (int)degrees(getCamRotation[0]), 30, 70);
  text("y: " + (int)degrees(getCamRotation[1]), 30, 90);
  text("z: " + (int)degrees(getCamRotation[2]), 30, 110);
  text("Camera position: ", 20, 140);
  text("x: " + (int)camPosition.x, 30, 160);
  text("y: " + (int)camPosition.y, 30, 180);
  text("z: " + (int)camPosition.z, 30, 200);
  cam.endHUD();
}