import serial
import time


def serial_setup(port: str, baud: int):
    ser = serial.Serial(port, baud, timeout=1)
    time.sleep(2)  # Arduino reset delay
    return ser


def send_command(ser, cmd: str) -> str:
    ser.write((cmd+"\n").encode())
    time.sleep(0.1)  # give arduino time
    response = ser.readline().decode().strip()
    return response


