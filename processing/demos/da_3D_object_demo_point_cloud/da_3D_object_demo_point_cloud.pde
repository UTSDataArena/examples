// Processing in the Data Arena
// 3D object mode sketches

// Point Cloud demo
// This demo introduces 3D sketches, using the drawContents() function from earlier
// Here we are drawing point cloud data into our scene
// And using the PeasyCam library to look and navigate
// Use Left/Right keys to change point density
// Use number keys to dial in point opacity

// Data source: The University of Osnabrück's Robotic 3D Scan Repository
// http://kos.informatik.uni-osnabrueck.de/3Dscans/

import peasy.*;
PeasyCam cam;

PGraphics contents;
String[] lines;
float x, y, z;
int r, g, b;
float opacity = 255;
float percent = 5;

void setup() {
  //size(10172, 2400, P3D); // Data Arena resolution
  size(1920, 2400, P3D); // Development resolution
  contents = createGraphics(width, height/2, P3D);
  cam = new PeasyCam(this, contents, 800);
  lines = loadStrings("scan_00.txt");
  imageMode(CORNER);
}

void drawContents(PGraphics pg) {
  pg.perspective(PI/3.0, (float)pg.width / (float)pg.height, 10, 1000000);
  pg.background(0);
  pg.pushMatrix();
  pg.translate(50, 0, 250);
  pg.rotateX(PI);
  for (int i = 0; i < lines.length; i += (int)100/percent) {
    String[] position = split(lines[i], " ");
    x = parseFloat(position[0]) * 10;
    y = parseFloat(position[1]) * 10;
    z = parseFloat(position[2]) * 10;
    r = parseInt(position[3]);
    g = parseInt(position[4]);
    b = parseInt(position[5]);
    pg.stroke(r, g, b, opacity);
    pg.point(x, y, z);
  }
  pg.popMatrix();

  cam.beginHUD();
  pg.translate(-width/2, 0);
  pg.scale(2);
  pg.fill(255);
  pg.noStroke();
  pg.text("FPS: " + (int)frameRate, 20, 20);
  int totalPoints = lines.length;
  int currentPoints = (int)(totalPoints * (percent/100));
  pg.text(currentPoints + " points", 20, 40);
  pg.text(percent + "% of " + totalPoints, 20, 60);
  cam.endHUD();
}

void draw() {
  background(0);
  contents.beginDraw();
  drawContents(contents);
  contents.endDraw();
  image(contents, 0, 0);
  image(contents, 0, height/2);
}

void keyPressed() {
  if (keyCode == LEFT) percent--;
  if (keyCode == RIGHT) percent++;
  if (key == '1') opacity = 20;
  if (key == '2') opacity = 45;
  if (key == '3') opacity = 80;
  if (key == '4') opacity = 105;
  if (key == '5') opacity = 130;
  if (key == '6') opacity = 155;
  if (key == '7') opacity = 180;
  if (key == '8') opacity = 205;
  if (key == '9') opacity = 230;
  if (key == '0') opacity = 255;
}