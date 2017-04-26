// Processing in the Data Arena
// 2D mode sketches

// Solar System demo
// This demo demonstrates how to use the drawContents() function
// to draw upper and lower copies of sketches with minimal code

import vrpn.*;
DeviceRead read;

PGraphics contents;
Table ssData;
String[] columnName = {"MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE"};
float timeScale = 1000000;

void setup() {
  //size(10172, 2400, P2D); // Data Arena resolution
  size(1920, 2400, P2D); // Development resolution
  contents = createGraphics(width, height/2, P2D);
  ssData = loadTable("ssStatsNasa.csv", "header");
  contents = createGraphics(width, height/2, P2D);

  read = new DeviceRead();
  read.vrpnSetup();
}

void drawContents(PGraphics pg) {
  updateTime();

  pg.translate(pg.width/2, pg.height/2);
  pg.colorMode(HSB, 360, 100, 100, 100);
  pg.background(0);

  pg.fill(40, 50, 100);
  pg.ellipse(0, 0, 150, 150);

  for (int i = 0; i < columnName.length; i++) {
    float diameter = ssData.getFloat(1, columnName[i]);
    float size = map(diameter, 1, 1391400, 1, 120);
    float meanTemp = ssData.getFloat(15, columnName[i]);
    float hue = map(meanTemp, -200, 464, 230, 0); 
    float orbitSize = map(i, 0, columnName.length, 150, 500);
    float orbitPeriod = ssData.getFloat(10, columnName[i]);
    float angle = degrees(ssData.getFloat(20, columnName[i]));
    angle += map(millis(), 0, (orbitPeriod*24*60*60*1000), 0, TWO_PI) * timeScale; 
    float x = sin(angle) * orbitSize;
    float y = cos(angle) * orbitSize;

    // draw orbit ring
    pg.noFill();
    pg.stroke(0, 0, 10);
    pg.strokeWeight(2);
    pg.ellipse(0, 0, orbitSize*2, orbitSize*2);

    // draw planet
    pg.noStroke();
    pg.fill(hue, 50, 100);
    pg.ellipse(x, y, size, size);
  }

  pg.fill(255);
  pg.textAlign(CENTER);
  pg.text("Sizes: to scale. Distances: not to scale", 0, pg.height/2-30);
  pg.text("Time adjustment: " + (int)timeScale + "x", 0, pg.height/2-10);
}

void draw() {
  background(0);
  contents.beginDraw();
  drawContents(contents);
  contents.endDraw();
  image(contents, 0, 0);
  image(contents, 0, height/2);
}

void updateTime() {
  timeScale += read.sprz * 10000;
}