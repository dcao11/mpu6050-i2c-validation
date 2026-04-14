from serial_comm import serial_setup, send_command
from analyzer import evaluate_result, analyze_i2c


def run_test(ser, cmd):
    print(f"\n[TEST] {cmd}")

    response = send_command(ser, cmd)
    print(f"Response: {response}")

    result = evaluate_result(response.split(":"))
    print(f"Result: {result}")

    return result


def run_i2c_analysis():
    print("\nRunning I2C Timing Analysis...\n")

    print("[100 kHz Test]")
    analyze_i2c('data/i2c_data_100khz.csv')

    print("\n[400 kHz Test]")
    analyze_i2c('data/i2c_data_400khz.csv')


def main():
    ser = serial_setup("COM3", 9600)

    commands = [
        "READ_WHOAMI",
        "READ_ACCEL",
        "READ_WHOAMI_BAD_ADDR"
    ]

    results = [run_test(ser, cmd) for cmd in commands]

    print("\n----------------------------------")
    print(f"PASS: {results.count('PASS')}")
    print(f"FAIL: {results.count('FAIL')}")
    print("----------------------------------")

    print("\n----------------------------------")

    run_i2c_analysis()


if __name__ == "__main__":
    main()

