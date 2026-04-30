SERIAL_PORT = "COM3"
BAUD_RATE = 9600

DATA_DIR_NAME = "data"
I2C_100KHZ_CSV = "data/i2c_data_100khz.csv"
I2C_400KHZ_CSV = "data/i2c_data_400khz.csv"

EXPECTED_WHO_AM_I = "104"  # 0x68 for MPU6050
MIN_Z_GRAVITY_LSB = 14000  # About 0.85g at default +/-2g scale