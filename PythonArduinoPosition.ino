/*******************************************************************************
* Copyright 2016 ROBOTIS CO., LTD.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

#include <Dynamixel2Arduino.h>


  #define DXL_SERIAL Serial1
  #define REC_SERIAL Serial
  const uint8_t DXL_DIR_PIN = 2; // DYNAMIXEL Shield DIR PIN

const uint8_t DXL_ID = 4;
const float DXL_PROTOCOL_VERSION = 2.0;

int debLED = 13;
String Str;

Dynamixel2Arduino dxl(DXL_SERIAL, DXL_DIR_PIN);

void setup() {
  // put your setup code here, to run once:
  
  // Use UART port of DYNAMIXEL Shield to debug.
  REC_SERIAL.begin(57600);

  pinMode(debLED, OUTPUT);

  // Set Port baudrate to 57600bps. This has to match with DYNAMIXEL baudrate.
  dxl.begin(57600);

  Serial2.begin(57600);

  
  // Set Port Protocol Version. This has to match with DYNAMIXEL protocol version.
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  // Get DYNAMIXEL information
  dxl.ping(DXL_ID);

  // Turn off torque when configuring items in EEPROM area
  dxl.torqueOff(DXL_ID);
  dxl.setOperatingMode(DXL_ID, OP_POSITION);
  dxl.torqueOn(DXL_ID);

}


void loop() {
Str="0";
  /*
  digitalWrite(debLED, HIGH);

 if(REC_SERIAL.available()>0){
  delay(50);
 Str = REC_SERIAL.readStringUntil('x');
 Serial2.print(Str);
 }
 */
 
//dxl.setGoalPosition(DXL_ID, 130, UNIT_DEGREE);
      //delay(1500);
//dxl.setGoalPosition(DXL_ID, 100, UNIT_DEGREE);
      //delay(1500);
 
  if(REC_SERIAL.available()>0){
    delay(100);
    Str = REC_SERIAL.readStringUntil('x');
   // Serial2.println("String: ");Serial2.print( Str);
    if(Str=="fist"){
      digitalWrite(debLED, LOW);
      Serial2.println("fist");
      delay(500);
    }
    else if(Str=="in"){
      Serial2.println("in");
      dxl.setGoalPosition(DXL_ID, 130, UNIT_DEGREE);
      
      //delay(1500);
    }
    else if(Str=="out"){
      Serial2.println("out");
      dxl.setGoalPosition(DXL_ID, 100, UNIT_DEGREE);
      //delay(1500);
    }
    else{
      digitalWrite(debLED, HIGH);
    }
  }

  
  //dxl.setGoalPosition(DXL_ID, 5.7, UNIT_DEGREE);
  //delay(1000);
  // Print present position in degree value
  
}
