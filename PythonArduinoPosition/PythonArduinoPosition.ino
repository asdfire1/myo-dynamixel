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

uint8_t DXL_ID = 4;
const float DXL_PROTOCOL_VERSION = 2.0;

int debLED = 13;
String Str;
int Opt = 0;
int pos = 150;

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
  dxl.ping(3);

  // Turn off torque when configuring items in EEPROM area
  //dxl.torqueOff(DXL_ID);
  //dxl.setOperatingMode(DXL_ID, OP_POSITION);
  //dxl.torqueOn(DXL_ID);

for(int i=1; i<=5; i++){
  dxl.torqueOff(i);
  dxl.setOperatingMode(i, OP_POSITION);
  dxl.torqueOn(i);
}

  pos = dxl.getPresentPosition(DXL_ID);
  
}

void loop() {

  switch(Opt)
    {
  
  case 1:
    digitalWrite(debLED, HIGH);
    if(DXL_ID==4){
      DXL_ID=1;
      pos = dxl.getPresentPosition(DXL_ID);
    }
    else{
      DXL_ID++;
      pos = dxl.getPresentPosition(DXL_ID);
    }
    Opt = 0;
    break;
  case 2:
    digitalWrite(debLED, HIGH);
    if(dxl.getPresentPosition(DXL_ID)-pos < 5){
    pos=pos+2;
    }
    else{
      pos = dxl.getPresentPosition(DXL_ID);
    }
    dxl.setGoalPosition(DXL_ID, pos);
    break;
  case 3:
    digitalWrite(debLED, HIGH);
    if(dxl.getPresentPosition(DXL_ID)-pos > -5){
    pos=pos-2;
    }
    else{
      pos = dxl.getPresentPosition(DXL_ID);
    }
    dxl.setGoalPosition(DXL_ID, pos);
    break;
  case 4:
    digitalWrite(debLED, HIGH);
    if(DXL_ID==1){
      DXL_ID=4;
      pos = dxl.getPresentPosition(DXL_ID);
    }
    else{
      DXL_ID--;
      pos = dxl.getPresentPosition(DXL_ID);
    }
    Opt = 0;
    break;
  default:
    digitalWrite(debLED, LOW);
    dxl.setGoalPosition(DXL_ID, pos);
 
  
}

if(REC_SERIAL.available()>0){
 delay(10);
 Str = REC_SERIAL.readStringUntil('x');
 Serial2.print(Str);
  
 if(Str=="fist"){
      digitalWrite(debLED, HIGH);
      Opt = 1;
    }
    else if(Str=="in"){
      digitalWrite(debLED, HIGH);
      Opt = 2;
    }
    else if(Str=="out"){
      digitalWrite(debLED, HIGH);
      Opt = 3;
    }
    else if(Str=="fingers"){
      digitalWrite(debLED, HIGH);
      Opt = 4;
    }
    else{
      digitalWrite(debLED, LOW);
      Opt = 0;
    }
  }


}
