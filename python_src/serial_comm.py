import serial
import time


def serial_setup(port: str, baud: int):
    try:
        ser = serial.Serial(port, baud, timeout=1)
    except serial.SerialException as exc:
        raise SystemExit(
            f"Could not open serial port {port} at {baud} baud: {exc}\n"
            "Close any Serial Monitor/PuTTY/PulseView session using the port, "
            "or rerun with the correct port, for example: python_src\\main.py --port COM4"
        ) from exc
    time.sleep(2)  # Arduino reset delay
    return ser


def send_command(ser, cmd: str) -> str:
    ser.write((cmd+"\n").encode())
    time.sleep(0.1)  # give arduino time
    response = ser.readline().decode().strip()
    return response


