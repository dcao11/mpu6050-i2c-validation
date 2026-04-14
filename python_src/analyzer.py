import pandas as pd


def evaluate_result(response: list[str]) -> str:
    status, test = response[0:2]

    if status == "ERR":
        return "FAIL"

    if test == "WHO_AM_I":
        return "PASS" if response[2] == "104" else "FAIL"

    if test == "ACCEL":
        z = int(response[4])
        return "PASS" if abs(z) > 14000 else "FAIL"

    return "FAIL"


def analyze_i2c(file_path):
    # Load the CSV
    df = pd.read_csv(file_path)

    # 1. Detect Time Unit from the first column name
    time_header = df.columns[0].lower()
    if 'nano' in time_header:
        multiplier = 1e-9  # Nanoseconds to Seconds
        unit = "Nanoseconds"
    elif 'micro' in time_header:
        multiplier = 1e-6  # Microseconds to Seconds
        unit = "Microseconds"
    elif 'milli' in time_header:
        multiplier = 1e-3  # Milliseconds to Seconds
        unit = "Milliseconds"
    else:
        multiplier = 1.0  # Assume Seconds
        unit = "Seconds"

    # 2. Identify Data Columns
    # If headers are 'logic, logic', Pandas renames the second one to 'logic.1'
    scl_col = df.columns[2]
    time_col = df.columns[0]

    # 3. Find Rising Edges of SCL (Transitions from 0 to 1)
    rising_edges = df[(df[scl_col] == 1) & (df[scl_col].shift(1) == 0)]

    if len(rising_edges) < 2:
        print("Error: Not enough clock pulses found to calculate frequency.")
        return

    # 4. Calculate Periods and Frequency
    # (Time_B - Time_A) * Multiplier = Period in Seconds
    periods_sec = rising_edges[time_col].diff().dropna() * multiplier

    # Filter out idle time (gaps larger than 1ms are usually between messages)
    valid_periods = periods_sec[periods_sec < 0.001]

    if valid_periods.empty:
        print("Error: No valid I2C traffic detected in the data.")
        return

    freq_khz = (1 / valid_periods) / 1000

    print(f"--- I2C Hardware Validation ---")
    print(f"Detected Unit:   {unit}")
    print(f"Mean Frequency:  {freq_khz.mean():.2f} kHz")
    print(f"Min Frequency:   {freq_khz.min():.2f} kHz")
    print(f"Max Frequency:   {freq_khz.max():.2f} kHz")
    print(f"Total Pulses:    {len(freq_khz)}")

