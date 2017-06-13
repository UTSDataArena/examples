// Processing in the Data Arena
// 3D Object Mode Sketches Template

import peasy.*;
PeasyCam cam;

// If you're in the Data Arena, set this to true
// and run matrix.solo.mono in a shell
boolean dataArena = false;

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
}

void draw() {
  background(0);
  fill(0);
  stroke(0, 255, 0);
  rotateY(radians(25));
  rotateX(radians(15));
  sphere(200);
}