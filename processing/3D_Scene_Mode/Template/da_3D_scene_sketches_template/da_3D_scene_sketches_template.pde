// Processing in the Data Arena
// 3D Scene Mode Sketches Template
// with over/under PGraphics windows

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

PGraphics contents;

// Camera
float[] getCamRotation, getCamPosition, getCamTarget;
PVector camDirection, camPosition, camTarget;
float camTranslateX, camTranslateY, camTranslateZ, camTranslateXLerp, camTranslateYLerp, camTranslateZLerp;
float camRotateX, camRotateY, camRotateZ, camRotateXLerp, camRotateYLerp, camRotateZLerp;
float lerpSpeed = 0.1;
float tranSen = 1;
float rotSen = 1;

void setup() {
  // As the Data Arena resolution is beyond usable
  // on regular monitors, leave the first size() function
  // commented until you're ready to test in the space

  // Remember to double the ordinary height of your sketch
  // to allow for over/under duplicates

  //size(10172, 2400, P3D); // Data Arena resolution
  size(1920, 2400, P3D); // Your development resolution

  // Here we set the contents graphics window to half height
  // so we can place it over and under
  // Half height of size() becomes your standard sketch height
  contents = createGraphics(width, height/2, P3D);

  cam = new PeasyCam(this, contents, 0, 0, 5000, 1);
  cam.setMinimumDistance(1);
  cam.setMaximumDistance(1);
  camDirection = new PVector();
  camPosition = new PVector();
  camTarget = new PVector();
}

void drawContents(PGraphics pg) {
  // Draw contents of your sketch here
  // rather than in the regular draw() function
  // This will let us easily copy the contents
  // to the top and bottom displays

  // Remember to run camUpdate in draw to refresh camera position
  updateCam();
  
  // Also, use the perspective() function to adjust your field of fiew
  // and the far clipping plane
  // You might want to test various FOV values in the Data Arena
  pg.perspective(PI/3.0, (float)pg.width / (float)pg.height, 10, 100000);

  pg.background(0);
  pg.stroke(0);
  pg.strokeWeight(2);
  randomSeed(1);
  for (int i = -2000; i < 2000; i += 100) {
    for (int j = -2000; j < 2000; j += 100) {
      pg.pushMatrix();
      pg.translate(i, j, 0);
      pg.fill(random(150, 255), random(150, 255), random(150, 255));
      pg.box(50);
      pg.popMatrix();
    }
  }

  printCamDetail(pg);
}

void draw() {
  // Now in draw we assign our PGraphics window
  // "contents" to the drawContents() function
  // within the standard PGraphics begin and end functions

  contents.beginDraw();
  drawContents(contents);
  contents.endDraw();

  // and use image() to draw our sketch to where we want
  // in this case both at 0, 0 and
  // halfway down at 0, height/2
  image(contents, 0, 0);
  image(contents, 0, height/2);
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
void printCamDetail(PGraphics pg) {
  float[] getCamRotation = cam.getRotations();
  cam.beginHUD();
  pg.translate(-pg.width/2, 0);
  pg.scale(2);
  pg.textSize(12);
  pg.fill(255);
  pg.text("Frames per second: " + (int)frameRate, 20, 20);
  pg.text("Camera rotations: ", 20, 50);
  pg.text("x: " + (int)degrees(getCamRotation[0]), 30, 70);
  pg.text("y: " + (int)degrees(getCamRotation[1]), 30, 90);
  pg.text("z: " + (int)degrees(getCamRotation[2]), 30, 110);
  pg.text("Camera position: ", 20, 140);
  pg.text("x: " + (int)camPosition.x, 30, 160);
  pg.text("y: " + (int)camPosition.y, 30, 180);
  pg.text("z: " + (int)camPosition.z, 30, 200);
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