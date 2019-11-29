#include <Dynamixel2Arduino.h> //Used for controlling the dynamixel servos
#include <Adafruit_NeoPixel.h> //Used for the indicator LEDs

  #define LEDPIN 3    //Pin that the indicator LEDs are connected to
  #define LEDNUM 24   //Number of NeoPixel LEDs

  #define DXL_SERIAL Serial1 //Serial that RS485 is connected to
  #define REC_SERIAL Serial //Serial from computer, receives data from myoband
  const uint8_t DXL_DIR_PIN = 2; // RS485 direction (LED) pin

  uint8_t DXL_ID = 4; //Starting id of a servo
  const float DXL_PROTOCOL_VERSION = 2.0;

  Adafruit_NeoPixel ledindicator(LEDNUM, LEDPIN, NEO_GRB + NEO_KHZ800); //Creating object for LEDs
  Dynamixel2Arduino dxl(DXL_SERIAL, DXL_DIR_PIN); //Creating object for dynamixel communication

void setup() {
  REC_SERIAL.begin(115200); //Computer serial baudrate, has to be the same as in our python code
  dxl.begin(115200); //Dynamixel baudrate, has to be the same as on the servos

  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);//Sets dynamixel protocol

 
  for(int i=1; i<=3; i++){ //We have 
    dxl.torqueOff(i);
    dxl.setOperatingMode(i, OP_VELOCITY); //Sets operating mode of dynamixels
    dxl.torqueOn(i);
  }
  for(int i=4; i<=5; i++){
    dxl.torqueOff(i);
    dxl.setOperatingMode(i, OP_VELOCITY); //Sets operating mode of dynamixels
    dxl.writeControlTableItem(VELOCITY_I_GAIN, i, 4000);
    dxl.writeControlTableItem(VELOCITY_P_GAIN, i, 300);
    dxl.torqueOn(i);
    } 

  ledindicator.begin(); // Initializes NeoPixel leds
  ledindicator.setBrightness(5); //Sets the brightness (can be changed)
  ledindicator.clear(); //Clears the currently displayed
  indicatorset();
}

void colorset(int a, int r, int g, int b){
  for(int i=a; i<(a+6); i++) { //For leds from a until a+6 (1/4 of the ring) a is 0 , 6, 12 , 18

    ledindicator.setPixelColor(i, ledindicator.Color(r,g,b));
  }
}

void indicatorset(){
    ledindicator.clear();
    colorset(0,255,0,0);
    if (DXL_ID > 1){
      colorset(6,0,255,0);
    }
    if(DXL_ID > 2){
    colorset(12,0,0,255);
    }
    if(DXL_ID > 3){
      colorset(18,255,255,255);
    }
    ledindicator.show();
}

void loop() {
  if(REC_SERIAL.available()>0){
    String Str = REC_SERIAL.readStringUntil('x');
  
  
    if(Str=="f"){
      dxl.writeControlTableItem(GOAL_VELOCITY, DXL_ID, 0);
      if(DXL_ID==4){
      DXL_ID=1;
        }
      else{
      DXL_ID++;
        }
      indicatorset();
      }
        
    else if(Str=="b"){
      dxl.writeControlTableItem(GOAL_VELOCITY, DXL_ID, 0);
      if(DXL_ID==1){
        DXL_ID=4;
        }
      else{
        DXL_ID--;
        }
      indicatorset();
      }
    else{  
      int musclestr=Str.toInt();
      if(DXL_ID!=4)
      musclestr=musclestr/2;
      dxl.writeControlTableItem(GOAL_VELOCITY, DXL_ID, musclestr);
    }
    
  }

}
