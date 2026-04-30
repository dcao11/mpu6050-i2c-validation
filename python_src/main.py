from serial_comm import serial_setup, send_command
from analyzer import evaluate_result, analyze_i2c
import time

def run_test(ser, cmd) -> str:
    print(f"\n[TEST] {cmd}")

    response = send_command(ser, cmd)
    print(f"Response: {response}")
    result = "FAIL"
    if ":" in response:
        result = evaluate_result(response.split(":"))
    elif response in ("PASS", "FAIL"):
        result = response
    print(f"Result: {result}")

    return result


def run_validation_suite(ser) -> list[str]:
    commands = [
        "READ_WHOAMI",
        "READ_ACCEL",
        "READ_WHOAMI_BAD_ADDR"
    ]

    results = [run_test(ser, cmd) for cmd in commands]

    print("\n----------------------------------")
    print(f"PASS: {results.count('PASS')}")
    print(f"FAIL: {results.count('FAIL')}")

    print("\n----------------------------------")

    return results


def run_i2c_analysis() -> None:
    print("\nRunning I2C Timing Analysis...\n")

    print("[100 kHz Test]")
    analyze_i2c('data/i2c_data_100khz.csv')

    print("\n[400 kHz Test]")
    analyze_i2c('data/i2c_data_400khz.csv')

    print("\n----------------------------------")


def read_diagnostic_block(ser, timeout_seconds: float = 5.0) -> None:
     # Diagnostics are multi-line, so read until the Arduino's end marker.
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        line = ser.readline().decode(errors="replace").strip()

        if not line:
            continue

        print(line)

        if line == "-----------------------":
            break
    else:
        print("ERR:I2C_DIAGNOSTICS_TIMEOUT")



def run_i2c_diagnostics(ser) -> None:
     # Set each I2C speed first, then request the register diagnostic block.
    diagnostic_tests = [
        ("SET_I2C_100K", "100 kHz"),
        ("SET_I2C_400K", "400 kHz")
    ]

    for set_clock_cmd, label in diagnostic_tests:
        print(f"\n[DIAGNOSTIC] {label}")
        ser.write((set_clock_cmd + "\n").encode())
        time.sleep(0.1)
        response = ser.readline().decode(errors="replace").strip()
        print(response)

        ser.write(("PRINT_I2C_DIAGNOSTICS\n").encode())
        time.sleep(0.1)
        read_diagnostic_block(ser)



def main():

    ser = serial_setup("COM3", 9600)
    # Clear any startup diagnostics printed by the Arduino after reset.
    ser.reset_input_buffer()
    run_validation_suite(ser)
    run_i2c_analysis()
    run_i2c_diagnostics(ser)


if __name__ == "__main__":
    main()
