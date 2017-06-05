// Processing in the Data Arena
// 3D Scene Mode sketch

// Solar System demo
// This sketch introduces 3D sketches in "scene" mode
// Compared to viewing 

// stars data source
// http://galaxymap.org/drupal/node/5

// Space Navigator controls
// translateY: move forward/backwards
// translateX: move left/right
// translateZ: move up/down
// rotateY: roll
// rotateX: pitch
// rotateZ: yaw

// Keyboard controls
// n: show/hide planet names
// l: show/hide orbit lines
// h: increase timescale
// g: decrease timescale
// -: decrease movement sensitivity
// =: increase movement sensitivity

import peasy.*;
import vrpn.*;

DeviceRead read;
PeasyCam cam;

// If you're in the Data Arena, set this to true
// and run matrix.solo.mono in a shell
boolean dataArena = false;

PGraphics contents;

boolean toScale = false;
boolean names = true;
boolean lines = true;

int speedTimer;
int speedTimerInterval = 100;

// Camera
float[] getCamRotation, getCamPosition, getCamTarget;
PVector camDirection, camPosition, camTarget;
float camTranslateX, camTranslateY, camTranslateZ, camTranslateXLerp, camTranslateYLerp, camTranslateZLerp;
float camRotateX, camRotateY, camRotateZ, camRotateXLerp, camRotateYLerp, camRotateZLerp;
float lerpSpeed = 0.1;
float tranSen = 1;
float rotSen = 0.25;
// For speed calculation
PVector latestRecordedPosition;
float speed;

// Stars
Table starsData;
ArrayList <Star> stars;

// Sun
PShape sun;
PImage sunTexture;
float sunRadius;

// Planets
Table planetData;
ArrayList<Planet> planets;
String[] planetNames = {"MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE"};
float time, timeScale, sizeScale, distScale;

PFont font;

void settings() {
  if (dataArena) {
    size(displayWidth, 1200, P3D);
  } else {
    // set your custom testing resolution here
    size(1920, 1200, P3D);
  }
}

void setup() {
  if (toScale) {
    cam = new PeasyCam(this, 0, 80000, 40000, 10);
  } else {
    cam = new PeasyCam(this, 0, 10000, 3000, 10);
  }
  cam.setMinimumDistance(10);
  cam.setMaximumDistance(10);
  cam.rotateX(radians(-75));
  camDirection = new PVector();
  camPosition = new PVector();
  camTarget = new PVector();
  latestRecordedPosition = new PVector();

  planetData = loadTable("solarSystemData.csv", "header");
  starsData = loadTable("galaxyMapData.csv", "header");
  font = loadFont("font.vlw");

  textFont(font);

  if (toScale) {
    timeScale = 1;
    distScale = 0.000719;
    sizeScale = 0.000719;
  } else {
    timeScale = 10000;
    distScale = 0.00001;
    sizeScale = 0.000719;
  }
  
  if (toScale) {
    println("MODE: TO SCALE");
    println("ONE UNIT = " + 1/distScale + "KM");
  }

  // Sun
  sphereDetail(60);
  sunTexture = loadImage("sunmap.jpg");
  sunRadius = (planetData.getFloat(1, "SUN")/2) * sizeScale;
  sun = createShape(SPHERE, sunRadius);
  println(sunRadius);
  sun.setTexture(sunTexture);
  sun.setStroke(false);

  stars = new ArrayList<Star>();
  int totalStars = starsData.getRowCount();
  for (int i = 0; i < totalStars; i++) {
    stars.add(new Star(i));
  }

  planets = new ArrayList<Planet>();
  for (int i = 0; i < planetNames.length; i++) {
    planets.add(new Planet(planetNames[i]));
  }
  
  read = new DeviceRead();
  read.vrpnSetup();
}

void draw() {
  updateCam();
  time = millis();

  if (dataArena) {
    perspective(PI/5.4, (float)width / (float)height, 10, 10000000);
  } else {
    perspective(PI/3.0, (float)width / (float)height, 10, 1000000);
  }
  
  background(0);
  noLights();
  pointLight(255, 255, 255, camPosition.x, camPosition.y, camPosition.z);
  pointLight(220, 220, 220, camPosition.x, camPosition.y, camPosition.z);
  shape(sun);
  noLights();
  for (Planet p : planets) {
    p.movePlanet();
    if (lines) p.displayOrbitGuide();
    p.displayPlanet();
    if (names) p.showLabels();
  }

  for (Star s : stars) {
    s.position();
    s.display();
  }
  
  printCamDetail();
}

void updateCam() {
  getCamPosition = cam.getLookAt();
  camPosition.x = getCamPosition[0];
  camPosition.y = getCamPosition[1];
  camPosition.z = getCamPosition[2];
  getCamTarget = cam.getPosition();
  camTarget.x = getCamTarget[0];
  camTarget.y = getCamTarget[1];
  camTarget.z = getCamTarget[2];
  
  camTranslateX = read.sptx*tranSen;
  camTranslateY = read.sptz*tranSen;
  camTranslateZ = -read.spty*(tranSen*3);
  camRotateX = -read.sprx*rotSen;
  camRotateY = -read.sprz*rotSen;
  camRotateZ = -read.spry*(rotSen/2);
  
  camDirection = PVector.sub(camPosition, camTarget);
  camDirection.normalize();
  camDirection.mult((camTranslateZ));
  camPosition.add(camDirection);
  cam.lookAt(camPosition.x, camPosition.y, camPosition.z, 0);
  cam.pan(camTranslateX, camTranslateY);
  
  cam.rotateX(radians(camRotateX));
  cam.rotateY(radians(camRotateY));
  cam.rotateZ(radians(camRotateZ));
}

void printCamDetail() {
  noLights();
  if (millis() - speedTimer >= speedTimerInterval) {
    speed = PVector.dist(latestRecordedPosition, camPosition) * (1000/speedTimerInterval);
    speed *= (1/distScale);
    latestRecordedPosition.x = camPosition.x;
    latestRecordedPosition.y = camPosition.y;
    latestRecordedPosition.z = camPosition.z;
    speedTimer = millis();
  }
  float[] getCamRotation = cam.getRotations();
  cam.beginHUD();
  perspective(PI/3.0, (float)width / (float)height, 10, 1000000);
  textSize(12);
  fill(255);
  text("Frames per second: " + (int)frameRate, 20, 20);
  text("Camera rotations: ", 20, 50);
  text("x: " + (int)degrees(getCamRotation[0]), 30, 70);
  text("y: " + (int)degrees(getCamRotation[1]), 30, 90);
  text("z: " + (int)degrees(getCamRotation[2]), 30, 110);
  text("Camera position: ", 20, 140);
  text("x: " + (int)camPosition.x, 30, 160);
  text("y: " + (int)camPosition.y, 30, 180);
  text("z: " + (int)camPosition.z, 30, 200);
  if (toScale) text("Speed: " + (int)speed + "km/s", 20, 230);
  cam.endHUD();
}

void keyPressed() {
  if (key == 'l') lines =! lines;
  if (key == 'n') names =! names;
  if (key == 'h') timeScale *= 2;
  if (key == 'g') timeScale /= 2;
  if (key == '-') tranSen /= 2;
  if (key == '=') tranSen *= 2;
}