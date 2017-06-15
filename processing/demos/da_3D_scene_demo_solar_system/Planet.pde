class Planet {
  String planetName;
  String nameShort;
  PShape planetShape;
  PImage planetTexture;
  float radius;
  float startPosition;
  float orbitRotation;
  float orbitalPeriod;
  float semiMajorAxis;
  float distance;
  float planetRotation;
  float dayLength;
  float x, y;

  // Saturn's rings
  int ringCount;
  String[] colours;
  int[] colourVal;
  float ringSize;
  float[] weight;
  int[] opacity;
  float gap = 120;

  Planet(String name) {
    sphereDetail(40);
    planetName = name;
    nameShort = planetName.substring(0, 3).toLowerCase();
    if (toScale) {
      radius = (planetData.getFloat(1, planetName)/2) * sizeScale;
    } else {
      radius = 50;
    }
    planetShape = createShape(SPHERE, radius);
    planetTexture = loadImage("../../resources/images/" + nameShort + ".jpg");
    planetShape.setStroke(false);
    planetShape.setTexture(planetTexture);
    startPosition = planetData.getFloat(20, planetName);
    orbitalPeriod = planetData.getFloat(10, planetName);
    dayLength = planetData.getFloat(6, planetName);
    semiMajorAxis = planetData.getFloat(7, planetName);
    distance = sunRadius + semiMajorAxis * distScale;

    if (planetName == "SATURN") {
      ringCount = 230;
      colourVal = new int[915];
      opacity = new int[ringCount];
      weight = new float[ringCount];
      ringSize = radius * 3;
      colours = loadStrings("../../resources/data/colours.txt");
      for (int i = 0; i < ringCount; i++) {
        weight[i] = random(3, 5);
        opacity[i] = (int)random(20, 80);
      }
    }
  }

  void displayOrbitGuide() {
    noFill();
    stroke(255, 30);
    strokeWeight(1);
    ellipse(0, 0, distance*2, distance*2);
  }

  void movePlanet() {
    orbitRotation = startPosition + map(time, 0, daysToMs(orbitalPeriod), 0, TWO_PI) * timeScale;
    planetRotation = map(time, 0, hrsToMs(dayLength), 0, TWO_PI) * timeScale;
    x = sin(orbitRotation) * distance;
    y = cos(orbitRotation) * distance;
  }

  void displayPlanet() {
    noLights();
    pointLight(255, 255, 255, 0, 0, 0);
    pushMatrix();
    translate(x, y, 0);
    rotateX(-HALF_PI);
    rotateY(planetRotation);
    shape(planetShape);
    if (planetName == "SATURN") {
      pushMatrix();
      rotateX(HALF_PI);
      for (int i = 0; i < ringCount; i++) {
        ringSize += radius/200;
        color c = int(colours[int(map(i, 0, ringCount, 0, colours.length))]);
        if (i < 80) {
          stroke(c, 70+i);
        } else if (i > 140 && i < 160) {
          stroke(c, 10);
        } else {
          stroke(c, opacity[i]+150);
        }
        strokeWeight(1);
        noFill();
        ellipse(0, 0, ringSize, ringSize);
      }
      ringSize = radius * 3;
      popMatrix();
    }
    popMatrix();
  }

  void showLabels() {
    noLights();
    pushMatrix();
    translate(x, y, 0);
    rotateX(cam.getRotations()[0]);
    rotateY(cam.getRotations()[1]);
    rotateZ(cam.getRotations()[2]);
    float d = dist(x, y, 0, cam.getPosition()[0], cam.getPosition()[1], cam.getPosition()[2]);
    float pointSize = map(d, 0, 50000, 0, 500)*0.7;
    float nameOpacity = map(d, 0, 5000, 0, 255);
    textSize(pointSize);
    fill(255, nameOpacity);
    text(planetName, radius + pointSize, 0);
    popMatrix();
  }

  float hrsToMs(float hrs) {
    float result = hrs*60*60*1000;
    return result;
  }

  float daysToMs(float days) {
    float result = days*24*60*60*1000;
    return result;
  }
}