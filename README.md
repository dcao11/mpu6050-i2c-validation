# I2C Validation Framework (MPU6050)

## Overview
Python-based validation framework communicating with Arduino firmware over serial to test MPU6050 via I2C.

## Features
- Serial command protocol
- I2C register + burst reads
- PASS/FAIL validation logic
- CSV logging
- Fault injection (bad address, bad data)

## Architecture
Python (Host) -> Serial -> Arduino (DUT) -> I2C -> MPU6050

## Commands
- READ_WHOAMI
- READ_ACCEL
- READ_WHOAMI_BAD_ADDR

## Example Output
OK:WHO_AM_I:104  
OK:ACCEL:-972:-52:15580  
ERR:I2C_FAIL  

## CSV Format
timestamp,result,command,status,test,x,y,z,raw

## Notes
Built to demonstrate validation engineering concepts: protocol design, automation, and fault injection.
