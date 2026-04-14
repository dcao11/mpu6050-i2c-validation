# I2C Validation Framework (MPU6050)

## Overview

Python-based validation framework for testing the MPU6050 sensor over
I2C using an Arduino as the device under test (DUT).

The system automates command execution, validates responses, and logs
structured results for analysis.

------------------------------------------------------------------------

## Features

-   Serial command protocol between Python host and Arduino DUT
-   I2C register access and burst reads
-   Automated PASS/FAIL evaluation logic
-   Structured CSV logging
-   Fault injection support (e.g. bad address, corrupted data)
-   Cross-platform file handling with dynamic path management

------------------------------------------------------------------------

## Architecture

Python (Host) -\> Serial -\> Arduino (DUT) -\> I2C -\> MPU6050

------------------------------------------------------------------------

## Project Structure

```
project_root/
│
├── python_src/                 # Python source code
│   ├── main.py          # Entry point
│   ├── serial_comm.py   # Serial communication
│   ├── logger.py        # CSV logging + test execution
│   ├── analyzer.py      # PASS/FAIL logic + analysis
│   └── config.py        # Configuration (paths, constants)
│
├── data/                # Generated CSV logs and pulse view csv files
│
├── arduino_src/             # Arduino firmware (DUT)
│   └── mpu6050_validation.ino
│
└── README.md
```

------------------------------------------------------------------------

## Commands

-   READ_WHOAMI
-   READ_ACCEL
-   READ_WHOAMI_BAD_ADDR

------------------------------------------------------------------------

## Example Output (Serial)

OK:WHO_AM_I:104 OK:ACCEL:-972:-52:15580 ERR:I2C_FAIL

------------------------------------------------------------------------

## CSV Logging

Format: timestamp, result, command, status, test, x, y, z, raw

Example: 

\['2026-04-04 17:39:40.805', 'PASS', 'READ_WHOAMI', 'OK',
'WHO_AM_I', '104', 'OK:WHO_AM_I:104'\]

\['2026-04-04 17:39:40.914', 'PASS', 'READ_ACCEL', 'OK', 'ACCEL',
'-928', '-176', '15168', 'OK:ACCEL:-928:-176:15168'\]

\['2026-04-04 17:39:41.023', 'FAIL', 'READ_WHOAMI_BAD_ADDR', 'ERR',
'MPU_NOT_DETECTED', 'ERR:MPU_NOT_DETECTED'\]

------------------------------------------------------------------------

## Validation Logic

-   Responses parsed and evaluated in analyzer.py
-   PASS/FAIL based on expected values and thresholds
-   Handles error and timeout conditions

------------------------------------------------------------------------

## Data Handling

-   Logs saved in data/ directory
-   Paths resolved dynamically using **file**
-   Directories auto-created if missing

------------------------------------------------------------------------

## Notes

Demonstrates validation engineering concepts: 
- Hardware/software
integration 
- Protocol design 
- Automation and logging 
- Fault injection 
- Data analysis

------------------------------------------------------------------------

## Future Improvements

-   Batch test runner
-   Summary report (PASS/FAIL stats)
-   I2C timing visualization
-   Mock serial testing
