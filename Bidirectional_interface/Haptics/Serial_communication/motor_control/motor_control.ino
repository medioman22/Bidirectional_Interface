#include <SoftwareSerial.h>

int rxPin = 13; //Warning, the pin 13 is also the pin linked to the ARDUINO's LED !! DO NOT USE THE LED !
int txPin = 12;// these are the digital pins used on the arduino to work as tx/rx on the bluetooth adapter
static byte tmp_input = 0; // temporary char to read from serial

SoftwareSerial newSerial(rxPin,txPin); 

int printToNewSerial = 0;
unsigned int counter = 0; // counts the received bytes
unsigned int received_data = 0; // it becomes 1 if the 'S' and 'E' chars are received
static byte input[4] = {0,0,0,0};      //Buffer to read from serial
unsigned int motor_to_activate = 0;





void setup() {
  // put your setup code here, to run once:
    pinMode(rxPin,INPUT);
    pinMode(txPin, OUTPUT);
    Serial.begin(9600);
    newSerial.begin(9600);

    pinMode(9,OUTPUT);
    pinMode(6,OUTPUT);
    pinMode(5,OUTPUT);
    pinMode(4,OUTPUT);
    pinMode(2,OUTPUT); // led
    digitalWrite(2,HIGH); // led
    
    // test motors
    analogWrite(6,200);
    analogWrite(9,200);
    analogWrite(5,200);
    analogWrite(3,200);
    delay(200);
        
    analogWrite(6,0);
    analogWrite(9,0);
    analogWrite(5,0);
    analogWrite(3,0);
      
    while (!newSerial) {
    ;
    }
    Serial.println("Serial available!");
}

void loop() {

  if(newSerial.available())
  {
    Serial.print("Recieving data\n");
    // get incoming byte
    tmp_input = newSerial.read();
    if (tmp_input == 83) // S start packet
    {
      counter = 0;
      Serial.print("Beginning\n");
    }
    else if(tmp_input == 69) // E end packet
    {
      counter++;
      received_data = 1;
      Serial.print("Ending\n");

    }
    else
    {
      Serial.println(tmp_input);
      input[counter] = tmp_input; // save the received bytes in this array
      counter++;
    }
  }

  if (received_data)
  {
    for (int i = 0; i < 4; ++i)
    {
      switch (i)
      {
        case 0:
          motor_to_activate = 6;
          break;
        case 1: 
          motor_to_activate = 9;
          break;
        case 2: 
          motor_to_activate = 5;
          break;
        case 3: 
          motor_to_activate = 3;
          break;
      }
        
      if (input[i] > 32)
      {
        analogWrite(motor_to_activate, input[i]);
      }
      else
      {
        analogWrite(motor_to_activate, 0);
      } 
      received_data = 0;
    }
  }
}


  
