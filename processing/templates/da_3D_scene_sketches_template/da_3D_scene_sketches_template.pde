// Processing in the Data Arena
// 3D Scene Mode Sketches Template

// Keyboard controls
// w: move forwards
// s: move backwards
// a: move left
// d: move right
// q: move up
// e: move down
// up arrow: look up
// down arrow: look down
// left arrow: look left
// right arrow: look right
// z: roll anti-clockwise
// x: roll clockwise

import peasy.*;
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
float tranSen = 1;
float rotSen = 1;

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
}

void draw() {
  // Remember to run camUpdate in draw to refresh camera position
  updateCam();
  
  // Also, use the perspective() function to adjust your field of fiew
  // and the far clipping plane
  // You might want to test various FOV values in the Data Arena
  if (dataArena) {
    perspective(PI/5.4, (float)width / (float)height, 10, 10000000);
  } else {
    perspective(PI/3.0, (float)width / (float)height, 10, 1000000);
  }

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
  
  // assign camera position and target values to our vectors
  getCamPosition = cam.getLookAt();
  camPosition.x = getCamPosition[0];
  camPosition.y = getCamPosition[1];
  camPosition.z = getCamPosition[2];
  getCamTarget = cam.getPosition();
  camTarget.x = getCamTarget[0];
  camTarget.y = getCamTarget[1];
  camTarget.z = getCamTarget[2];
  
  // update translation and rotate values with certain keys
  if (keyPressed) {
    if (key == 'w') camTranslateZ += 1 * tranSen;
    if (key == 's') camTranslateZ -= 1 * tranSen;
    if (key == 'd') camTranslateX += 1 * tranSen;
    if (key == 'a') camTranslateX -= 1 * tranSen;
    if (key == 'q') camTranslateY += 1 * tranSen;
    if (key == 'e') camTranslateY -= 1 * tranSen;
    if (keyCode == UP) camRotateX = -1 * rotSen;
    if (keyCode == DOWN) camRotateX = 1 * rotSen;
    if (keyCode == RIGHT) camRotateY = -1 * rotSen;
    if (keyCode == LEFT) camRotateY = 1 * rotSen;
    if (key == 'z') camRotateZ = -1 * rotSen;
    if (key == 'x') camRotateZ = 1 * rotSen;
  }

  // interpolate values for smoother easing motion
  camTranslateXLerp = lerp(camTranslateXLerp, camTranslateX, lerpSpeed);
  camTranslateYLerp = lerp(camTranslateYLerp, camTranslateY, lerpSpeed);
  camTranslateZLerp = lerp(camTranslateZLerp, camTranslateZ, lerpSpeed);
  camRotateXLerp = lerp(camRotateXLerp, camRotateX, lerpSpeed);
  camRotateYLerp = lerp(camRotateYLerp, camRotateY, lerpSpeed);
  camRotateZLerp = lerp(camRotateZLerp, camRotateZ, lerpSpeed);

  // set camera position
  camDirection = PVector.sub(camPosition, camTarget);
  camDirection.normalize();
  camDirection.mult((camTranslateZLerp));
  camPosition.add(camDirection);
  cam.lookAt(camPosition.x, camPosition.y, camPosition.z, 0);
  cam.pan(camTranslateXLerp, camTranslateYLerp);

  // set camera rotations
  cam.rotateX(radians(camRotateXLerp));
  cam.rotateY(radians(camRotateYLerp));
  cam.rotateZ(radians(camRotateZLerp));
}

// this function demonstrates displaying on-screen graphics
// or a heads-up display
void printCamDetail() {
  float[] getCamRotation = cam.getRotations();
  cam.beginHUD();
  perspective(PI/3.0, (float)width / (float)height, 10, 1000000);
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

// use KeyReleased() to stop culmulative rotations
void keyReleased() {
  if (key == 'w') camTranslateZ = 0;
  if (key == 's') camTranslateZ = 0;
  if (key == 'd') camTranslateX = 0;
  if (key == 'a') camTranslateX = 0;
  if (key == 'q') camTranslateY = 0;
  if (key == 'e') camTranslateY = 0;
  if (keyCode == UP) camRotateX = 0;
  if (keyCode == DOWN) camRotateX = 0;
  if (keyCode == RIGHT) camRotateY = 0;
  if (keyCode == LEFT) camRotateY = 0;
  if (key == 'z') camRotateZ = 0;
  if (key == 'x') camRotateZ = 0;
}