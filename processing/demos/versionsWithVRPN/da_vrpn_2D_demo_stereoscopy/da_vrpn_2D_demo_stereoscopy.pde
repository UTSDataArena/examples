// Processing in the Data Arena
// 2D mode sketches

// Stereoscopy
// This demo introduces stereoscopic visuals in 2D environments
// made possible with duel PGraphics contexts
// Here we need to make sure the sketch is double the intended vertical resolution
// as we'll be generating two copies, stacked.

import vrpn.*;
DeviceRead read;

// If you're in the Data Arena, set this to true
// and run matrix.solo in a shell
boolean dataArena = false;
int xStart, xEnd, yStart, yEnd;

PGraphics contentsTop, contentsBottom;
float counter;
int noiseMax;
color col1, col2;
int hue1, hue2;
int weight;

void settings() {
  if (dataArena) {
    size(displayWidth, 2400, P2D);
  } else {
    // set your custom testing resolution here
    // make sure it's double due to the over/under system
    size(1920, 2400, P2D);
  }
}

void setup() {
  contentsTop = createGraphics(width, height/2, P2D);
  contentsBottom = createGraphics(width, height/2, P2D);
  colorMode(HSB, 360, 100, 100, 100);

  if (dataArena) {
    // these values are calibrated according to
    // the projector adjustments of late May 2017.
    // They may need to change with future adjustments
    xStart = 83;
    xEnd = 10659;
    yStart = 0;
    yEnd = contentsTop.height;
    weight = 2;
  } else {
    xStart = 0;
    xEnd = contentsTop.width;
    yStart = 0;
    yEnd = contentsTop.height;
    weight = 1;
  }
  
  noiseMax = -388;
  col1 = color(330, 40, 100);
  col2 = color(190, 40, 100);
  
  read = new DeviceRead();
  read.vrpnSetup();
}

void drawContents(PGraphics pg, float eyeOffset) {
  pg.smooth();
  pg.colorMode(HSB, 360, 100, 100, 100);
  pg.strokeWeight(weight);
  pg.background(0);

  counter += 0.005;

  pg.noFill();
  
  int totalLines = 30;
  int distFromCentre = 200;
  noiseMax += (read.sprz*5);
  float middle = (contentsTop.height/2) - (noiseMax/2);

  for (int l = 0; l < totalLines; l++) {
    pg.stroke(lerpColor(col1, col2, map(l, 0, totalLines, 0, 1)));
    pg.beginShape();
    for (float k = xStart; k < xEnd; k += 50) {
      float n = noise(k/33 + counter) * noiseMax;
      float xPos = k + (map(n, 0, noiseMax, 0, eyeOffset));
      float yPos = map(l, 0, totalLines, middle - distFromCentre, middle + distFromCentre) + n;
      pg.curveVertex(xPos, yPos);
    }
    pg.endShape();
  }
}

void draw() {
  contentsTop.beginDraw();
  drawContents(contentsTop, 8);
  contentsTop.endDraw();

  contentsBottom.beginDraw();
  drawContents(contentsBottom, -8);
  contentsBottom.endDraw();

  image(contentsTop, 0, 0);
  image(contentsBottom, 0, height/2);
}