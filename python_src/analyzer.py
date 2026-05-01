import pandas as pd
import os
from config import EXPECTED_WHO_AM_I, MIN_Z_GRAVITY_LSB


def evaluate_result(response: list[str]) -> str:
    if len(response) < 2:
        return "FAIL"

    status = response[0]
    command = response[1]

    if command == "READ_WHOAMI_BAD_ADDR":
        return "PASS" if response == ["ERR", "READ_WHOAMI_BAD_ADDR", "MPU_NOT_DETECTED"] else "FAIL"

    if status == "ERR":
        return "FAIL"

    if command == "READ_WHOAMI":
        if len(response) < 4:
            return "FAIL"
        return "PASS" if response[2] == "WHO_AM_I" and response[3] == EXPECTED_WHO_AM_I else "FAIL"

    if command == "READ_ACCEL":
        if len(response) < 6 or response[2] != "ACCEL":
            return "FAIL"
        z = int(response[5])
        return "PASS" if abs(z) > MIN_Z_GRAVITY_LSB else "FAIL"

    return "FAIL"


def analyze_i2c(file_path: str) -> None:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    full_path = os.path.join(base_dir, file_path)

    df = pd.read_csv(full_path)

    time_col = df.columns[0]
    scl_col = df.columns[2]

    time_header = time_col.lower()
    if "nano" in time_header:
        multiplier = 1e-9
        unit = "Nanoseconds"
    elif "micro" in time_header:
        multiplier = 1e-6
        unit = "Microseconds"
    elif "milli" in time_header:
        multiplier = 1e-3
        unit = "Milliseconds"
    else:
        multiplier = 1.0
        unit = "Seconds"

    rising_edges = df[(df[scl_col] == 1) & (df[scl_col].shift(1) == 0)]

    if len(rising_edges) < 2:
        print("Error: Not enough clock pulses found to calculate frequency.")
        return

    periods_sec = rising_edges[time_col].diff().dropna() * multiplier
    valid_periods = periods_sec[periods_sec < 0.001]

    if valid_periods.empty:
        print("Error: No valid I2C traffic detected in the data.")
        return

    freq_khz = (1 / valid_periods) / 1000

    print("--- I2C Hardware Validation ---")
    print(f"File:            {os.path.basename(file_path)}")
    print(f"Detected Unit:   {unit}")
    print(f"Mean Frequency:  {freq_khz.mean():.2f} kHz")
    print(f"Min Frequency:   {freq_khz.min():.2f} kHz")
    print(f"Max Frequency:   {freq_khz.max():.2f} kHz")
    print(f"Total Pulses:    {len(freq_khz)}")