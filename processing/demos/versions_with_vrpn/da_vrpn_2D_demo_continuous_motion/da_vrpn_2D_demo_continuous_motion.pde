// Processing in the Data Arena
// 2D mode sketches

// Continuous Motion demo
// This demo introduces continuous motion with minimal stutter
// near the entrance door projector overlap

import vrpn.*;
DeviceRead read;

PGraphics contents;
ArrayList<Dot> dots;

void setup() {
  //size(10172, 2400, P2D); // Data Arena resolution
  size(1920, 2400, P2D); // Development resolution
  contents = createGraphics(width, height/2, P2D);
  dots = new ArrayList<Dot>();
  for (int i = 0; i < 500; i++) {
    dots.add(new Dot());
  }
  
  read = new DeviceRead();
  read.vrpnSetup();
}

void drawContents(PGraphics pg) {
  pg.background(0);
  for (Dot d : dots) {
    d.move();
    d.display();
  }
}

void draw() {
  contents.beginDraw();
  drawContents(contents);
  contents.endDraw();
  image(contents, 0, 0);
  image(contents, 0, height/2);
}

class Dot {
  float xPos = random(width);
  float yPos = random(height);
  float speed = random(0.5, 10);
  float size = random(7);
  float opacity = random(150, 255);

  void move() {
    speed += read.sprz;
    xPos += speed;
    //if (xPos > 9849+180) xPos = 135; // da size
    if (xPos > width) xPos = 0;
    if (xPos < 0) xPos = width;
  }

  void display() {
    fill(255, opacity);
    ellipse(xPos, yPos, size, size);
  }
}