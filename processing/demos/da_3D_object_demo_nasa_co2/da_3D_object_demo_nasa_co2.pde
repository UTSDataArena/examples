// Processing in the Data Arena
// 3D object mode sketches

// NASA CO2 demo
// This demo continues 3D sketches, using the drawContents() function from earlier
// Here we've wrapped a CO2 data video from NASA GISS around a spherical object
// PeasyCam is used to centre in on this subject, allowing for rotation around the object

// Data source: NASA GISS
// https://www.youtube.com/watch?v=x1SgmFa0r04

import processing.video.*;
import peasy.*;

PeasyCam cam;
Movie co2vid;
Movie timescale;

// If you're in the Data Arena, set this to true
// and run matrix.solo.mono in a shell
boolean dataArena = false;

PShape globe;
boolean play = true;
String[] monthNames = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"};
float guiStart;
float guiEnd;
PImage co2scale;

void settings() {
  if (dataArena) {
    size(displayWidth, 1200, P3D);
  } else {
    // set your custom testing resolution here
    size(1920, 1200, P3D);
  }
}

void setup() {
  cam = new PeasyCam(this, 800);
  co2vid = new Movie(this, "../../media/video/nasaco2.mkv");
  co2vid.loop();
  globe = createShape(SPHERE, 200);
  globe.setTexture(co2vid);
  globe.setStroke(false);

  textureMode(NORMAL);
  imageMode(CORNER);
  textAlign(CENTER);
  textSize(10);

  guiStart = width/2-400;
  guiEnd = width/2-25;
  co2scale = loadImage("scale.jpg");
}

void draw() {
  background(0);
  drawGlobe();
  drawHUD();
}

void drawGlobe() {
  cam.beginHUD();
  directionalLight(255, 255, 255, 0.5, 0.5, -1); 
  cam.endHUD();
  shape(globe);
}

void drawHUD() {
  noLights();
  cam.beginHUD();
  noFill();
  stroke(100);
  line(guiStart-10, height-60, guiEnd+10, height-60);
  noStroke();
  fill(255);
  ellipse(map(co2vid.time(), 0, co2vid.duration(), guiStart, guiEnd), height-60, 4, 4);
  textAlign(CENTER);
  for (int i = 0; i < monthNames.length; i++) {
    float x = map(i, 0, monthNames.length-1, guiStart, guiEnd);
    String monthName = monthNames[i].toUpperCase();
    text(monthName, x, height-40);
  }
  textAlign(LEFT);
  text("2006", guiStart-10, height-75);
  text("Carbon Dioxide Column Concentration [ppmv]", width/2+25, height-75);
  image(co2scale, width/2+25, height-62, ((width/2+400)-(width/2+25)), 5);
  for (int i = 0; i < 10; i++) {
    float x = map(i, 0, 9, width/2+25, width/2+400);
    float value = map(i, 0, 9, 377, 395);
    text((int)value, x, height-40);
  }
  cam.endHUD();
}

void movieEvent(Movie m) {
  m.read();
}

void mouseClicked() {
  if (mouseY > height-100) {
    co2vid.jump(map(mouseX, guiStart, guiEnd, 0, co2vid.duration()));
  }
}