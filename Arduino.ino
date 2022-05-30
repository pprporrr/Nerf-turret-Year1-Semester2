#include <Servo.h>
#include <Wire.h>
#include <VL53L0X.h>

VL53L0X sensor;
Servo recoil_servo;
Servo pan_servo;
Servo tilt_servo;

#define HIGH_ACCURACY

const char in1=5;
const char in2=6;
const char in3=7;
const char in4=8;

const byte pan_limit_1 = 71;
const byte pan_limit_2 = 112;
const byte tilt_limit_1 = 114;
const byte tilt_limit_2 = 130;
const byte recoil_rest = 180;    
const byte recoil_pushed = 125; 

byte byte_from_app;
const byte buffSize = 15;
byte inputBuffer[buffSize];
const byte startMarker = 255;
const byte endMarker = 254;
byte bytesRecvd = 0;
boolean data_received = false;

bool is_firing =  false;
bool can_fire =  false;
bool recoiling = false;

unsigned long firing_start_time = 0;
unsigned long firing_current_time = 0;
const long firing_time = 150;

unsigned long recoil_start_time = 0;
unsigned long recoil_current_time = 0;
const long recoil_time = 2 * firing_time;

const byte motor_pin =  12;
const byte laser_light = 4 ;
const byte eyes_light = 3 ;
boolean motors_ON = false;
int i,j;

void setup()
{
  pinMode(motor_pin, OUTPUT);
  digitalWrite(motor_pin, LOW);
  pinMode(laser_light,OUTPUT);
  digitalWrite(laser_light,HIGH);
  pinMode(eyes_light,OUTPUT);
  digitalWrite(eyes_light,LOW);

  recoil_servo.attach(9);
  pan_servo.attach(10);
  tilt_servo.attach(11);

  recoil_servo.write(recoil_rest);
  pan_servo.write(90);
  delay(1000);
  tilt_servo.write(120);

  pinMode(in1,OUTPUT);
  pinMode(in2,OUTPUT);  
  pinMode(in3,OUTPUT);  
  pinMode(in4,OUTPUT); 
  i=0,j=1;
  Serial.begin(9600);

void loop()
{
  getDataFromPC();
  digitalWrite(12,inputBuffer[2]);
  if (data_received){
    digitalWrite(12,inputBuffer[2]);
    move_wheel();
    move_servo();
    set_recoil();
  }
  fire();
  
}

void getDataFromPC() {
  if (Serial.available()) {  

    byte_from_app = Serial.read();   

    if (byte_from_app == 255) {     
      bytesRecvd = 0;                   
      data_received = false;
    }

    else if (byte_from_app == 254) {   
      data_received = true; 
      Serial.print("\n");
    }

    else {                            
      inputBuffer[bytesRecvd] = byte_from_app;
      Serial.print(byte_from_app);
      Serial.print(" ");
      bytesRecvd++;                                
      if (bytesRecvd == buffSize) { 
        bytesRecvd = buffSize - 1;    
      }
    }
  }
}

void move_servo() {
  byte pan_servo_position = map(inputBuffer[i], 0, 240, pan_limit_2, pan_limit_1);
  pan_servo.write(pan_servo_position); 
  byte tilt_servo_position = map(inputBuffer[j], 0 , 240, tilt_limit_2, tilt_limit_1); 
  tilt_servo.write(tilt_servo_position);
  
}

void set_recoil() {
  if (inputBuffer[3] == 1) {       
    if (!is_firing && !recoiling) { 
      can_fire = true;              
    }
  }
  else {                  
    can_fire = false; 
  }
  
}

void set_motor() {
  if (inputBuffer[2]) {               
    digitalWrite(motor_pin, HIGH);          
  }
  else {                          
    digitalWrite(motor_pin, LOW);         
  }
  
}

void fire() { 
  if (can_fire && !is_firing) {
  {
    firing_start_time = millis();
    recoil_start_time = millis();
    is_firing = true;
  }

  firing_current_time = millis();
  recoil_current_time = millis();

  if (is_firing && firing_current_time - firing_start_time < firing_time) {
    recoil_servo.write(recoil_pushed);
  }
  else if (is_firing && recoil_current_time - recoil_start_time < recoil_time) {
    recoil_servo.write(recoil_rest);
  }
  else if (is_firing && recoil_current_time - recoil_start_time > recoil_time) {
    is_firing = false;
  }

}

void move_wheel() {
 if(inputBuffer[4]==1){
    digitalWrite(in1,0);
    digitalWrite(in2,1);
    digitalWrite(in3,0);
    digitalWrite(in4,1);
 }else if(inputBuffer[4]==4){
    digitalWrite(in1,0);
    digitalWrite(in2,1);
    digitalWrite(in3,1);
    digitalWrite(in4,0);

 }else if(inputBuffer[4]==2){
    digitalWrite(in1,1);
    digitalWrite(in2,0);
    digitalWrite(in3,0);
    digitalWrite(in4,1);
    
 }else if(inputBuffer[4]==3){
    digitalWrite(in1,1);
    digitalWrite(in2,0);
    digitalWrite(in3,1);
    digitalWrite(in4,0);
 }
 else if(inputBuffer[4]==0){
    digitalWrite(in1,0);
    digitalWrite(in2,0);
    digitalWrite(in3,0);
    digitalWrite(in4,0);
 }
 
}
