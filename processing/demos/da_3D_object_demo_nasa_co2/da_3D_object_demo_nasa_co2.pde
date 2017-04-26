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

PGraphics contents;

PShape globe;
boolean play = true;
String[] monthNames = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"};
float guiStart;
float guiEnd;
PImage co2scale;

void setup() {
  //size(10172, 2400, P3D); // Data Arena resolution
  size(1920, 2400, P3D); // Development resolution
  contents = createGraphics(width, height/2, P3D);
  cam = new PeasyCam(this, contents, 800);
  co2vid = new Movie(this, "nasaco2.mp4");
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

void drawContents(PGraphics pg) {
  
  pg.background(0);
  pg.noLights();
  cam.beginHUD();
  pg.translate(-width/2, 0);
  pg.scale(2);
  pg.noFill();
  pg.stroke(100);
  pg.line(guiStart-10, pg.height-60, guiEnd+10, pg.height-60);
  pg.noStroke();
  pg.fill(255);
  pg.ellipse(map(co2vid.time(), 0, co2vid.duration(), guiStart, guiEnd), pg.height-60, 4, 4);
  pg.textAlign(CENTER);
  for (int i = 0; i < monthNames.length; i++) {
    float x = map(i, 0, monthNames.length-1, guiStart, guiEnd);
    String monthName = monthNames[i].toUpperCase();
    pg.text(monthName, x, pg.height-40);
  }
  pg.textAlign(LEFT);
  pg.text("2006", guiStart-10, pg.height-75);
  pg.text("Carbon Dioxide Column Concentration [ppmv]", width/2+25, height-75);
  pg.image(co2scale, pg.width/2+25, pg.height-62, ((pg.width/2+400)-(pg.width/2+25)), 5);
  for (int i = 0; i < 10; i++) {
    float x = map(i, 0, 9, pg.width/2+25, pg.width/2+400);
    float value = map(i, 0, 9, 377, 395);
    pg.text((int)value, x, pg.height-40);
  }
  cam.endHUD();
  
  cam.beginHUD();
  pg.directionalLight(255, 255, 255, 0.5, 0.5, -1);
  cam.endHUD();
  pg.shape(globe);
}

void draw() {
  contents.beginDraw();
  drawContents(contents);
  contents.endDraw();
  image(contents, 0, 0);
  image(contents, 0, height/2);
}
// remove this after making vrpn version
//void updateCam() {
//  dist += (spty*50);
//  rotY = sprz*0.05;
//  rotX = -sprx*0.01;
//  rotZ = spry*0.01;
//  cam.rotateY(rotY);
//  cam.rotateX(rotX);
//  cam.rotateZ(rotZ);
//  //cam.setDistance(dist, 1);
//}

void movieEvent(Movie m) {
  m.read();
}

void mouseClicked() {
  if (mouseY > height-100) {
    co2vid.jump(map(mouseX, guiStart, guiEnd, 0, co2vid.duration()));
  }
}