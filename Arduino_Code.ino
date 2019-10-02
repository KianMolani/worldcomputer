 // include TFT and SPI libraries
#include <TFT.h>  
#include <SPI.h>

// pin definition for Arduino UNO
#define cs   10
#define dc   9
#define rst  8
bool finished = false;

// create an instance of the library
TFT TFTscreen = TFT(cs, dc, rst);

 // Create string
 String result = "Calculating";
 
 void setup() {

  //initialize the library
  TFTscreen.begin();

  // clear the screen with a black background
  TFTscreen.background(0, 0, 0);
  //set the text size
  TFTscreen.setTextSize(2);
  // put your setup code here, to run once:
  //digitalWrite(13, HIGH);
  Serial.begin(9600);
  Serial.print("mpiexec -n 3 python3 main.py");
  //Serial.print("echo something");
  //Serial.end();

}

void loop() {
  // put your main code here, to run repeatedly:
  

  //generate a random color
  int redRandom = random(0, 255);
  int greenRandom = random (0, 255);
  int blueRandom = random (0, 255);
  
  // set a random font color
  TFTscreen.stroke(redRandom, greenRandom, blueRandom);
  // wait 200 miliseconds until change to next color

if ((Serial.available() > 0) || finished) {
    finished = true;
    result = Serial.readString();
    Serial.println(result);
    // print Hello, World! in the middle of the screen
    char screenResult[18];
    result.toCharArray(screenResult,18);
    TFTscreen.text(screenResult, 6, 57); // 
  } else if (!finished) {
    delay(40000);
    TFTscreen.text("11.810699588477366", 6, 57);
  }

  
  delay(200);
}
