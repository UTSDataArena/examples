class Star {

  PVector coordinates;
  PVector position;
  float latitude, longitude;
  float starMapRadius;
  float size;
  float brightness;

  Star(int row) {
    coordinates = new PVector();
    latitude = starsData.getFloat(row, "Latitude");
    longitude = starsData.getFloat(row, "Longitude");
    starMapRadius = 500000;
    size = random(2);
    brightness = random(255);
  }
  
  void position() {
    position = sphericalToCartesian(longitude, latitude);
  }
  
  void display() {
    stroke(255, brightness);
    strokeWeight(size);
    point(position.x, position.y, position.z);
  }

  PVector sphericalToCartesian(float longitude, float latitude) {
    float latitudeAngle = radians(latitude);
    float longitudeAngle = radians(longitude);
    float x = cam.getPosition()[0] + starMapRadius * cos(latitudeAngle) * cos(longitudeAngle);
    float y = cam.getPosition()[1] + starMapRadius * cos(latitudeAngle)* sin(longitudeAngle);
    float z = cam.getPosition()[2] + starMapRadius * sin(latitudeAngle);
    PVector coords = new PVector(x, y, z);
    return coords;
  }
}