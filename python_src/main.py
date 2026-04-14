from logger import send_command_csv
from analyzer import analyze_i2c
from serial_comm import serial_setup, send_command
import os



# print(__file__)
# print(os.path.dirname(__file__))
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# DATA_DIR = os.path.join(BASE_DIR, "data")
# print(BASE_DIR)
# print(DATA_DIR)


# serial_setup("COM3",9600)
# print(send_command("SET_I2C_100K"))
# send_command_csv("READ_WHOAMI")
# send_command_csv("READ_ACCEL")
# send_command_csv("READ_WHOAMI_BAD_ADDR")
# print(send_command("SET_I2C_400K"))
# send_command_csv("READ_WHOAMI")
# send_command_csv("READ_ACCEL")
# send_command_csv("READ_WHOAMI_BAD_ADDR")


# for i in range(100):
#     send_command_csv("READ_ACCEL")

# analyze_i2c('i2c_data_100khz.csv')
# analyze_i2c('i2c_data_400khz.csv')



