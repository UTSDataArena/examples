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

  Planet(String name, PGraphics pg) {
    pg.sphereDetail(40);
    planetName = name;
    nameShort = planetName.substring(0, 3).toLowerCase();
    if (toScale) {
      radius = (planetData.getFloat(1, planetName)/2) * sizeScale;
    } else {
      radius = 50;
    }
    planetShape = createShape(SPHERE, radius);
    planetTexture = loadImage(nameShort + ".jpg");
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
      colours = loadStrings("colours.txt");
      for (int i = 0; i < ringCount; i++) {
        weight[i] = random(3, 5);
        opacity[i] = (int)random(20, 80);
      }
    }
  }

  void displayOrbitGuide(PGraphics pg) {
    pg.noFill();
    pg.stroke(255, 30);
    pg.strokeWeight(1);
    pg.ellipse(0, 0, distance*2, distance*2);
  }

  void movePlanet(PGraphics pg) {
    orbitRotation = startPosition + map(time, 0, daysToMs(orbitalPeriod), 0, TWO_PI) * timeScale;
    planetRotation = map(time, 0, hrsToMs(dayLength), 0, TWO_PI) * timeScale;
    x = sin(orbitRotation) * distance;
    y = cos(orbitRotation) * distance;
  }

  void displayPlanet(PGraphics pg) {
    pg.noLights();
    pg.pointLight(255, 255, 255, 0, 0, 0);
    pg.pushMatrix();
    pg.translate(x, y, 0);
    pg.rotateX(-HALF_PI);
    pg.rotateY(planetRotation);
    pg.shape(planetShape);
    if (planetName == "SATURN") {
      pg.pushMatrix();
      pg.rotateX(HALF_PI);
      for (int i = 0; i < ringCount; i++) {
        ringSize += radius/200;
        color c = int(colours[int(map(i, 0, ringCount, 0, colours.length))]);
        if (i < 80) {
          pg.stroke(c, 70+i);
        } else if (i > 140 && i < 160) {
          pg.stroke(c, 10);
        } else {
          pg.stroke(c, opacity[i]+150);
        }
        pg.strokeWeight(1);
        pg.noFill();
        pg.ellipse(0, 0, ringSize, ringSize);
      }
      ringSize = radius * 3;
      pg.popMatrix();
    }
    pg.popMatrix();
  }

  void showLabels(PGraphics pg) {
    pg.noLights();
    pg.pushMatrix();
    pg.translate(x, y, 0);
    pg.rotateX(cam.getRotations()[0]);
    pg.rotateY(cam.getRotations()[1]);
    pg.rotateZ(cam.getRotations()[2]);
    float d = dist(x, y, 0, cam.getPosition()[0], cam.getPosition()[1], cam.getPosition()[2]);
    float pointSize = map(d, 0, 50000, 0, 500);
    float nameOpacity = map(d, 0, 5000, 0, 255);
    pg.textSize(pointSize);
    pg.fill(255, nameOpacity);
    pg.text(planetName, radius + pointSize, 0);
    pg.popMatrix();
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