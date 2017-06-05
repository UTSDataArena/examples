// Processing in the Data Arena
// 2D Sketches Template

// If you're in the Data Arena, set this to true
// and run matrix.solo.mono in a shell
boolean dataArena = false;
int xStart, xEnd, yStart, yEnd;

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
  if (dataArena) {
    // Use these values for wrapping graphics.
    // They are calibrated according to the
    // projector adjustments of late May 2017.
    // They may need to change with future adjustments.
    xStart = 83;
    xEnd = 10659;
    yStart = 0;
    yEnd = height;
  } else {
    xStart = 0;
    xEnd = width;
    yStart = 0;
    yEnd = height;
  }
}

void draw() {
  background(0);
  stroke(0, 255, 0);
  noFill();
  rectMode(CENTER);
  
  translate(width/2, height/2);
  rotate(radians(frameCount));
  rect(0, 0, 100, 100);
  ellipse(0, 0, 50, 50);
}