// Processing in the Data Arena
// 2D Sketches Template
// with over/under PGraphics windows

PGraphics contents;

void setup() {
  // As the Data Arena resolution is beyond usable
  // on regular monitors, leave the first size() function
  // commented until you're ready to test in the space
  
  // Remember to double the ordinary height of your sketch
  // to allow for over/under duplicates
  
  //size(10172, 2400, P2D); // Data Arena resolution
  size(1920, 2400, P2D); // Your development resolution
  
  // Here we set the contents graphics window to half height
  // so we can place it over and under
  // Half height of size() becomes your standard sketch height
  contents = createGraphics(width, height/2, P2D);
}

void drawContents(PGraphics pg) {
  // Draw contents of your sketch here
  // rather than in the regular draw() function
  // This will let us easily copy the contents
  // to the top and bottom displays
  
  pg.background(0);
  pg.stroke(0, 255, 0);
  pg.noFill();
  pg.rectMode(CENTER);
  
  pg.translate(pg.width/2, pg.height/2);
  pg.rotate(radians(frameCount));
  pg.rect(0, 0, 100, 100);
  pg.ellipse(0, 0, 50, 50);
  
  // Door area
  // When running in the DA at the full resolution
  // This section will make visible the projector overlap
  // at the entrance door
  
  //pg.fill(0, 0, 255);
  //pg.rect(0, 0, 266, pg.height);
  //pg.fill(255, 0, 0);
  //pg.rect(9849, 0, pg.width-9849, pg.height);
  
  // See the second 2D sketch DA demo for creating continuous 360 motion
  
  
}

void draw() {
  // Now in draw we assign our PGraphics window
  // "contents" to the drawContents() function
  // within the standard PGraphics begin and end functions
  contents.beginDraw();
  drawContents(contents);
  contents.endDraw();
  
  // and use image() to draw our sketch to where we want
  // in this case both at 0, 0 and
  // halfway down at 0, height/2
  image(contents, 0, 0);
  image(contents, 0, height/2);
}