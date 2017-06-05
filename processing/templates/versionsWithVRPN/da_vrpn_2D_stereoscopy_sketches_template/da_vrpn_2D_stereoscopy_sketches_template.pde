// Processing in the Data Arena
// 2D Stereoscopic Sketches Template
// with VRPN connection support

// This example uses the 3D Connexion Space Navigator
// to shift layers and depth.

import vrpn.*;
DeviceRead read;

// If you're in the Data Arena, set this to true
// and run matrix.solo.mono in a shell
boolean dataArena = false;
int xStart, xEnd, yStart, yEnd;

PGraphics contentsTop, contentsBottom;
ArrayList<Square> squares;
float sizeControl;

void settings() {
  if (dataArena) {
    // size will be detected automagically
    size(displayWidth, 2400, P2D);
  } else {
    // set your custom testing resolution here
    size(1920, 2400, P2D);
  }
}

void setup() {
  contentsTop = createGraphics(width, height/2, P2D);
  contentsBottom = createGraphics(width, height/2, P2D);

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

  squares = new ArrayList<Square>();
  for (int i = 0; i < 20; i++) {
    squares.add(new Square(i));
  }

  read = new DeviceRead();
  read.vrpnSetup();
}

void drawContents(PGraphics pg, float eyeOffset) {
  pg.background(0);
  pg.stroke(0, 255, 0);
  pg.noFill();
  pg.rectMode(CENTER);
  pg.translate(contentsTop.width/2, contentsTop.height/2);

  sizeControl += read.sprz * 0.025;
  if (sizeControl > 1) sizeControl = 1;
  if (sizeControl < 0) sizeControl = 0;
  println(sizeControl);

  for (Square s : squares) {
    s.move();
    s.display(pg, eyeOffset);
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

class Square {

  float originalxPos;
  float xPos;
  float yPos;
  float size;
  float minSize;
  float maxSize;
  float offset;
  boolean even;

  Square(int i) {
    originalxPos = map(i, 0, 20, -500, 500);
    xPos = originalxPos;
    yPos = 0;
    minSize = 1;
    maxSize = 50;
    if (i % 2 == 0) {
      even = true;
    } else {
      even = false;
    }
  }

  void move() {
    if (even) {
      size = map(sizeControl, 0, 1, minSize, maxSize);
    } else {
      size = map(sizeControl, 0, 1, maxSize, minSize);
    }
  }

  void display(PGraphics pg, float eyeOffset) {
    offset = map(size, minSize, maxSize, 0, eyeOffset);
    xPos = originalxPos + offset;
    pg.rect(xPos, yPos, size, size);
  }
}