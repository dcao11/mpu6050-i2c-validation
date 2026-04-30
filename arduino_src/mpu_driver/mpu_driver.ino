#include <Wire.h>
#include <stdint.h>

// registers 
const uint8_t ADDR_MPU6050 = 0x68;

const uint8_t REG_PWR_MGMT_1 = 0x6B;
const uint8_t REG_WHO_AM_I = 0x75;

const uint8_t REG_ACCEL_XOUT = 0x3B; //[15:8], 0x3C is [7:0] likewise for the other accelerometer 
const uint8_t REG_ACCEL_YOUT = 0x3D;
const uint8_t REG_ACCEL_ZOUT = 0x3F;

uint32_t current_i2c_hz = 400000;


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

void printI2CDiagnostics(uint32_t requested_hz) {
  const uint32_t PCLKB_HZ = R_FSP_SystemClockHzGet(FSP_PRIV_CLOCK_PCLKB);
  const uint32_t SCI_CLOCK_HZ = R_FSP_SystemClockHzGet(BSP_FEATURE_SCI_CLOCK);
  const uint32_t IICPHI_HZ = PCLKB_HZ;

  uint8_t icfer = R_IIC1->ICFER;
  uint8_t icmr1 = R_IIC1->ICMR1;
  uint8_t icmr3 = R_IIC1->ICMR3;
  uint8_t brl = R_IIC1->ICBRL & 0x1F;
  uint8_t brh = R_IIC1->ICBRH & 0x1F;

  bool scle = (icfer >> 6) & 1;
  bool nfe = (icfer >> 5) & 1;
  uint8_t cks = (icmr1 >> 4) & 0x07;
  uint8_t nf = icmr3 & 0x03;

  Serial.println();
  Serial.println("--- I2C diagnostics ---");
  Serial.print("Requested clock Hz: "); Serial.println(requested_hz);
  Serial.print("PCLKB Hz: "); Serial.println(PCLKB_HZ);
  Serial.print("BSP_FEATURE_SCI_CLOCK Hz: "); Serial.println(SCI_CLOCK_HZ);

  Serial.print("ICFER=0x"); Serial.print(icfer, HEX);
  Serial.print(" SCLE="); Serial.print(scle);
  Serial.print(" NFE="); Serial.println(nfe);

  Serial.print("ICMR1=0x"); Serial.print(icmr1, HEX);
  Serial.print(" CKS="); Serial.print(cks, BIN); Serial.println("b");

  Serial.print("ICMR3=0x"); Serial.print(icmr3, HEX);
  Serial.print(" NF="); Serial.println(nf);

  Serial.print("ICBRL="); Serial.print(brl);
  Serial.print(" ICBRH="); Serial.println(brh);

  uint8_t nf_cycles = nfe ? (nf + 1) : 0;
  uint16_t high_cycles = brh + 3 + nf_cycles;
  uint16_t low_cycles = brl + 3 + nf_cycles;
  uint16_t total_cycles = high_cycles + low_cycles;
  uint32_t iic_clock_hz = IICPHI_HZ >> cks;
  float high_ns = (1000000000.0f * high_cycles) / iic_clock_hz;
  float low_ns = (1000000000.0f * low_cycles) / iic_clock_hz;
  float base_rate_hz = (float) iic_clock_hz / total_cycles;

  Serial.print("Formula case: SCLE=");
  Serial.print(scle);
  Serial.print(", NFE=");
  Serial.print(nfe);
  Serial.print(", CKS=");
  Serial.print(cks, BIN); Serial.println("b");

  Serial.print("Estimated high cycles: "); Serial.println(high_cycles);
  Serial.print("Estimated low cycles: "); Serial.println(low_cycles);
  Serial.print("Estimated total cycles before tr/tf: "); Serial.println(total_cycles);
  Serial.print("IICphi Hz used for estimate: "); Serial.println(IICPHI_HZ);
  Serial.print("IICphi divided by CKS Hz: "); Serial.println(iic_clock_hz);
  Serial.print("Base high ns before tr: "); Serial.println(high_ns);
  Serial.print("Base low ns before tf: "); Serial.println(low_ns);
  Serial.print("Base rate Hz before tr/tf: "); Serial.println(base_rate_hz);
  Serial.println("Use: rate = 1 / ((total_cycles / IICphi) + tr + tf)");
  Serial.println("-----------------------");
}


void setup() {
  Serial.begin(9600);
  while (!Serial);
  Wire.begin();

  Wire.setClock(current_i2c_hz);
  delay(1000);

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
      current_i2c_hz = 100000;
      Wire.setClock(current_i2c_hz);
      Serial.println("OK:CLK=100kHz");
    }
    else if (serial_input == "SET_I2C_400K") {
      current_i2c_hz = 400000;
      Wire.setClock(current_i2c_hz);
      Serial.println("OK:CLK=400kHz");
    }
    else if (serial_input == "PRINT_I2C_DIAGNOSTICS") {
      printI2CDiagnostics(current_i2c_hz);
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


// Reads 16-bit register from starting with first 8 bit register
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
