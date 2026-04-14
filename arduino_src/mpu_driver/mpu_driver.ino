#include <Wire.h>
#include <stdint.h>

// registers 
const uint8_t ADDR_MPU6050 = 0x68;

const uint8_t REG_PWR_MGMT_1 = 0x6B;
const uint8_t REG_WHO_AM_I = 0x75;

const uint8_t REG_ACCEL_XOUT = 0x3B; //[15:8], 0x3C is [7:0] likewise for the other accelerometer 
const uint8_t REG_ACCEL_YOUT = 0x3D;
const uint8_t REG_ACCEL_ZOUT = 0x3F;


struct Result8 {
    bool success;
    uint8_t value;
};

struct Result16 {
    bool success;
    int16_t value;
};

struct BurstResult6 {
    bool success;
    uint8_t data[6];
};


void setup() {
  Serial.begin(9600);
  while (!Serial);
  Wire.begin();

  // Wake up the sensor
  writeRegister(ADDR_MPU6050,REG_PWR_MGMT_1, 0x00);
}

void loop() {
  if (Serial.available()){
    String serial_input = Serial.readStringUntil('\n');
    serial_input.trim();
    if (serial_input =="READ_WHOAMI"){
      Result8 RES_WHO_AM_I = readRegister8(ADDR_MPU6050,REG_WHO_AM_I);
      if (RES_WHO_AM_I.success){
        Serial.print("OK:WHO_AM_I:");
        Serial.println(RES_WHO_AM_I.value);
      }
      else{
        Serial.println("ERR:MPU_NOT_DETECTED");
      }
    }
    else if(serial_input =="READ_ACCEL"){
      BurstResult6 RES_ACCEL = readBurst6(ADDR_MPU6050, REG_ACCEL_XOUT);
      if (RES_ACCEL.success){
        int16_t RES_ACCEL_XOUT = (RES_ACCEL.data[0] << 8) | RES_ACCEL.data[1];
        int16_t RES_ACCEL_YOUT = (RES_ACCEL.data[2] << 8) | RES_ACCEL.data[3];
        int16_t RES_ACCEL_ZOUT = (RES_ACCEL.data[4] << 8) | RES_ACCEL.data[5];
        Serial.print("OK:ACCEL:"); 
        Serial.print(RES_ACCEL_XOUT);
        Serial.print(":"); 
        Serial.print(RES_ACCEL_YOUT);
        Serial.print(":"); 
        Serial.println(RES_ACCEL_ZOUT);
      }
      else{
        Serial.println("ERR:FAILED_READ_ACCEL");
      }
    }
    else if (serial_input =="READ_WHOAMI_BAD_ADDR"){
      Result8 RES_WHO_AM_I = readRegister8(ADDR_MPU6050 + 1,REG_WHO_AM_I);
      if (RES_WHO_AM_I.success){
        Serial.print("OK:WHO_AM_I:");
        Serial.println(RES_WHO_AM_I.value);
      }
      else{
        Serial.println("ERR:MPU_NOT_DETECTED");
      }
    }
    else if (serial_input == "SET_I2C_100K") {
    Wire.setClock(100000);
    Serial.println("OK:CLK=100kHz");
    }
    else if (serial_input == "SET_I2C_200K") {
    Wire.setClock(200000);
    Serial.println("OK:CLK=200kHz");
    }
    else if (serial_input == "SET_I2C_300K") {
    Wire.setClock(300000);
    Serial.println("OK:CLK=300kHz");
    }
    else if (serial_input == "SET_I2C_400K") {
    Wire.setClock(400000);
    Serial.println("OK:CLK=400kHz");
    }
    else if (serial_input == "SET_I2C_1000K") {
    Wire.setClock(1000000);
    Serial.println("OK:CLK=1000kHz");
    }
    else{
      Serial.println("ERR:UNKNOWN_CMD");
    }
  }
}



// Reads a single 8-bit register from a specific address
Result8 readRegister8(uint8_t device_addr, uint8_t reg) {
  Result8 default_value = {false, 0};  // start with failed case

  Wire.beginTransmission(device_addr);
  Wire.write(reg);

  if (Wire.endTransmission(false) != 0) {  // 0 = success
    return default_value;
  }

  if (Wire.requestFrom(device_addr, 1) != 1) {  // expect 1 byte
    return default_value;
  }

  uint8_t val = Wire.read();
  return {true, val};
}



Result16 readRegister16(uint8_t device_addr, uint8_t reg){
  Result16 default_value = {false, 0};  // start with failed case

  Wire.beginTransmission(device_addr);
  Wire.write(reg);
  if (Wire.endTransmission(false) != 0) {  // 0 = success
    return default_value;
  }

  if (Wire.requestFrom(device_addr, 2) != 2) {  // expect 1 byte
    return default_value;
  }

  uint8_t MSB = Wire.read();
  uint8_t LSB = Wire.read();
  int16_t val = (int16_t)((MSB << 8)|LSB);
  return {true, val};
}



// reading multiple register at once to reduce overhead 
BurstResult6 readBurst6(uint8_t device_addr, uint8_t reg) {
  BurstResult6 default_value = {false, {0, 0, 0, 0, 0, 0}};

  Wire.beginTransmission(device_addr);
  Wire.write(reg);

  if (Wire.endTransmission(false) != 0) {
    return default_value;
  }

  if (Wire.requestFrom(device_addr, 6) != 6) {
    return default_value;
  }

  default_value.success = true;

  for (uint8_t i = 0; i < 6; i++) {
    default_value.data[i] = Wire.read();
  }

  return default_value;
}



// helper function to write to a specific 8 bit register
void writeRegister(uint8_t device_addr, uint8_t reg, uint8_t val) {
  Wire.beginTransmission(device_addr);
  Wire.write(reg);
  Wire.write(val);
  Wire.endTransmission();
}




