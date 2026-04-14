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

### Example Logged Output (Python / CSV)
['2026-04-04 17:39:40.805', 'PASS', 'READ_WHOAMI', 'OK', 'WHO_AM_I', '104', 'OK:WHO_AM_I:104']

['2026-04-04 17:39:40.914', 'PASS', 'READ_ACCEL', 'OK', 'ACCEL', '-928', '-176', '15168', 'OK:ACCEL:-928:-176:15168']

['2026-04-04 17:39:41.023', 'FAIL', 'READ_WHOAMI_BAD_ADDR', 'ERR', 'MPU_NOT_DETECTED', 'ERR:MPU_NOT_DETECTED']

## Notes
Built to demonstrate validation engineering concepts: protocol design, automation, and fault injection.
