// Processing in the Data Arena
// 2D mode sketches
// with VRPN connection support

// This example uses the 3D Connexion Space Navigator
// to control a cursor with the joystick
// and to place birds with the left button
// Reset the cursor with the right button.

// Flocking demo
// This demo also introduces continuous motion with minimal stutter
// near the entrance door projector overlap

/**
 * Flocking 
 * by Daniel Shiffman.  
 * 
 * An implementation of Craig Reynold's Boids program to simulate
 * the flocking behavior of birds. Each boid steers itself based on 
 * rules of avoidance, alignment, and coherence.
 * 
 */

import vrpn.*;
DeviceRead read;

float cursorX, cursorY;

// If you're in the Data Arena, set this to true
// and run matrix.solo.mono in a shell
boolean dataArena = true;
int xStart, xEnd, yStart, yEnd;

Flock flock;

void settings() {
  if (dataArena) {
    size(displayWidth, 1200, P2D);
  } else {
    // set your custom testing resolution here
    size(1920, 1200, P2D);
  }
}

void setup() {
  background(0);

  if (dataArena) {
    // these values are calibrated according to
    // the projector adjustments of late May 2017.
    // They may need to change with future adjustments
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

  colorMode(HSB, 360, 100, 100, 100);
  cursorX = width/2;
  cursorY = height/2;

  flock = new Flock();
  for (int i = 0; i < 500; i++) {
    flock.addBoid(new Boid(width/2, height/2));
  }

  read = new DeviceRead();
  read.vrpnSetup();
}

void draw() {
  updateCursor();
  fill(0, 0, 0, 60);
  noStroke();
  rect(0, 0, width, height);
  flock.run();
  if (read.button1) {
    flock.addBoid(new Boid(cursorX, cursorY));
  }
}

void updateCursor() {
  cursorX += (read.sptx*40);
  cursorY += (read.spty*40);
  if (cursorX > xEnd) cursorX = xStart;
  if (cursorX < xStart) cursorX = xEnd;
  if (cursorY > yEnd) cursorY = yStart;
  if (cursorY < yStart) cursorY = yEnd;
  noFill();
  stroke(0, 0, 100);
  line(cursorX-10, cursorY, cursorX+10, cursorY);
  line(cursorX, cursorY-10, cursorX, cursorY+10);
  if (read.button2) {
    cursorX = width/2;
    cursorY = height/2;
  }
}