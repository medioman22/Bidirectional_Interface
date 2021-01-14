#include <SPI.h>

const int CS1_pin = 9; // SPI Digital Potentiometer 1 ChipSelect signal (active LOW)
const int CS2_pin = 8; // SPI Digital Potentiometer 2 ChipSelect signal (active LOW)
const int HV1_pin = 7; // enable pin for HV1 power supply
const int HV2_pin = 6; // enable pin for HV2 power supply
const int OUT5_pin = 10; // half-bridge4 control pin
const int OUT4_pin = 5; // half-bridge4 control pin
const int OUT3_pin = 4; // half-bridge3 control pin
const int OUT2_pin = 3; // half-bridge2 control pin
const int OUT1_pin = 2; // half-bridge1 control pin
int nbytes;
char command;
int value = 0;
int command_received = 0;
char char_used;   // for incoming serial data
char char_unused;   // for incoming serial data

//int analogPin = A1;

void setup()
{
  pinMode(CS1_pin, OUTPUT);
  digitalWrite(CS1_pin, HIGH);
  pinMode(CS2_pin, OUTPUT);
  digitalWrite(CS2_pin, HIGH);
  digitalWrite(HV1_pin, LOW);
  pinMode(HV1_pin, OUTPUT);
  pinMode(HV2_pin, OUTPUT);
  digitalWrite(HV2_pin, LOW);
  pinMode(OUT1_pin, OUTPUT);
  digitalWrite(OUT1_pin, LOW);
  pinMode(OUT2_pin, OUTPUT);
  digitalWrite(OUT2_pin, LOW);
  pinMode(OUT3_pin, OUTPUT);
  digitalWrite(OUT3_pin, LOW);
  pinMode(OUT4_pin, OUTPUT);
  digitalWrite(OUT4_pin, LOW);
  pinMode(A1,OUTPUT);
  digitalWrite(A1,0);

  Serial.begin(115200);  // Begin the serial monitor at 115200bps
  SPI.begin();

  Voltage1Write(250); // set low voltage 1 (right) to approx 2.5V (for 5V put 19, for 0.9V put 250) old value - 100
  // 40-550,65-500,105-450,135-400,165-350,190-300,220-250,240-200,250-170
  Voltage2Write(251); // set low voltage 2 (left) to approx 2.5V (for 5V put 6, for 0.9V put 251) old value - 100
  // 20-550,55-500,90-450,125-400,160-350,185-300,215-250,240-200,251-170
  digitalWrite(HV1_pin, 1);
  digitalWrite(HV2_pin, 1);
  InitSnake2(); // fancy LED sequence
}


void loop()
{
  if (Serial.available()>0)
  {
    command = Serial.read();
    switch (command){
    case '0':
      digitalWrite(OUT1_pin, 0);
      digitalWrite(OUT2_pin, 0);
      digitalWrite(OUT3_pin, 0);
      digitalWrite(OUT4_pin, 0);
      digitalWrite(OUT5_pin, 0);
      break;
    case 'a':
      digitalWrite(OUT1_pin, 1);
      digitalWrite(OUT2_pin, 0);
      digitalWrite(OUT3_pin, 0);
      digitalWrite(OUT4_pin, 0);
      digitalWrite(OUT5_pin, 1);
      break;
    case 'b':
      digitalWrite(OUT1_pin, 0);
      digitalWrite(OUT2_pin, 1);
      digitalWrite(OUT3_pin, 0);
      digitalWrite(OUT4_pin, 0);
      digitalWrite(OUT5_pin, 1);
      break;
    case 'c':
      digitalWrite(OUT1_pin, 1);
      digitalWrite(OUT2_pin, 1);
      digitalWrite(OUT3_pin, 0);
      digitalWrite(OUT4_pin, 0);
      digitalWrite(OUT5_pin, 1);
      break;
    case 'd':    
      digitalWrite(OUT1_pin, 0);
      digitalWrite(OUT2_pin, 0);
      digitalWrite(OUT3_pin, 1);
      digitalWrite(OUT4_pin, 0);
      digitalWrite(OUT5_pin, 1);
      break;
    case 'e':
      digitalWrite(OUT1_pin, 1);
      digitalWrite(OUT2_pin, 0);
      digitalWrite(OUT3_pin, 1);
      digitalWrite(OUT4_pin, 0);
      digitalWrite(OUT5_pin, 1);
      break;
    case 'f':
      digitalWrite(OUT1_pin, 0);
      digitalWrite(OUT2_pin, 1);
      digitalWrite(OUT3_pin, 1);
      digitalWrite(OUT4_pin, 0);
      digitalWrite(OUT5_pin, 1);
      break;
    case 'g':
      digitalWrite(OUT1_pin, 1);
      digitalWrite(OUT2_pin, 1);
      digitalWrite(OUT3_pin, 1);
      digitalWrite(OUT4_pin, 0);
      digitalWrite(OUT5_pin, 1);
      break;
    case 'h':
      digitalWrite(OUT1_pin, 0);
      digitalWrite(OUT2_pin, 0);
      digitalWrite(OUT3_pin, 0);
      digitalWrite(OUT4_pin, 1);
      digitalWrite(OUT5_pin, 1);
      break;
    case 'i':
      digitalWrite(OUT1_pin, 1);
      digitalWrite(OUT2_pin, 0);
      digitalWrite(OUT3_pin, 0);
      digitalWrite(OUT4_pin, 1);
      digitalWrite(OUT5_pin, 1);
      break;
    case 'j':
      digitalWrite(OUT1_pin, 0);
      digitalWrite(OUT2_pin, 1);
      digitalWrite(OUT3_pin, 0);
      digitalWrite(OUT4_pin, 1);
      digitalWrite(OUT5_pin, 1);
      break;
    case 'k':
      digitalWrite(OUT1_pin, 1);
      digitalWrite(OUT2_pin, 1);
      digitalWrite(OUT3_pin, 0);
      digitalWrite(OUT4_pin, 1);
      digitalWrite(OUT5_pin, 1);
      break;
    case 'l':
      digitalWrite(OUT1_pin, 0);
      digitalWrite(OUT2_pin, 0);
      digitalWrite(OUT3_pin, 1);
      digitalWrite(OUT4_pin, 1);
      digitalWrite(OUT5_pin, 1);
      break;
    case 'm':
      digitalWrite(OUT1_pin, 1);
      digitalWrite(OUT2_pin, 0);
      digitalWrite(OUT3_pin, 1);
      digitalWrite(OUT4_pin, 1);
      digitalWrite(OUT5_pin, 1);
      break;
    case 'n':
      digitalWrite(OUT1_pin, 0);
      digitalWrite(OUT2_pin, 1);
      digitalWrite(OUT3_pin, 1);
      digitalWrite(OUT4_pin, 1);
      digitalWrite(OUT5_pin, 1);
      break;
    case 'o':
      digitalWrite(OUT1_pin, 1);
      digitalWrite(OUT2_pin, 1);
      digitalWrite(OUT3_pin, 1);
      digitalWrite(OUT4_pin, 1);
      digitalWrite(OUT5_pin, 1);
      break;
    default:
      break;
    }
  }
  // and loop forever and ever!
}

//++++++++++++++++++++++++++++++++++++++++++++ DO NOT MODIFY BELOW +++++++++++++++++++++++++++++++++++++++++++++++++++

void Voltage1Write(int value) {
  digitalWrite(CS1_pin, LOW);
  delay(10);
  SPI.transfer(value);
  delay(10);
  digitalWrite(CS1_pin, HIGH);
}

void Voltage2Write(int value) {
  digitalWrite(CS2_pin, LOW);
  delay(10);
  SPI.transfer(value);
  delay(10);
  digitalWrite(CS2_pin, HIGH);
}

void InitSnake(void){ //use only when HV1 and HV2 are disabled
  delay(100);
  digitalWrite(OUT1_pin, HIGH);
  delay(100);
  digitalWrite(OUT2_pin, HIGH);
  delay(100);
  digitalWrite(OUT3_pin, HIGH);
  delay(100);
  digitalWrite(OUT4_pin, HIGH);
  delay(100);
  digitalWrite(OUT1_pin, LOW);
  delay(100);
  digitalWrite(OUT2_pin, LOW);
  delay(100);
  digitalWrite(OUT3_pin, LOW);
  delay(100);
  digitalWrite(OUT4_pin, LOW);
}
void InitSnake2(void){ //use only when HV1 and HV2 are disabled
  delay(100);
  digitalWrite(OUT1_pin, HIGH);
  delay(100);
  digitalWrite(OUT2_pin, HIGH);
  digitalWrite(OUT1_pin, LOW);
  delay(100);
  digitalWrite(OUT3_pin, HIGH);
  digitalWrite(OUT2_pin, LOW);
  delay(100);
  digitalWrite(OUT4_pin, HIGH);
  digitalWrite(OUT3_pin, LOW);
  delay(100);
  digitalWrite(OUT3_pin, HIGH);
  digitalWrite(OUT4_pin, LOW);
  delay(100);
  digitalWrite(OUT2_pin, HIGH);
  digitalWrite(OUT3_pin, LOW);
  delay(100);
  digitalWrite(OUT1_pin, HIGH);
  digitalWrite(OUT2_pin, LOW);
  delay(100);
  digitalWrite(OUT1_pin, LOW);
}
