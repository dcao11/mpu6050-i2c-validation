from datetime import datetime
import csv
import os
from serial_comm import send_command
from analyzer import evaluate_result

def get_precise_time() -> str:
    # 1. Get the raw float timestamp
    raw_ts = time.time()
    # 2. Convert to a datetime object
    dt_object = datetime.fromtimestamp(raw_ts)
    # 3. Format it as a string
    precise_date = dt_object.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return precise_date


def send_command_csv(cmd: str) -> None:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    os.makedirs(DATA_DIR, exist_ok=True)

    precise_time: str = get_precise_time()
    data: str = send_command(cmd)

    file_name = os.path.join(DATA_DIR, f"test_{cmd}.csv")
    file_exists = os.path.isfile(file_name)

    header_map = {
        "READ_WHOAMI": ["timestamp", "result", "command", "status", "test", "val", "raw"],
        "READ_ACCEL": ["timestamp", "result", "command", "status", "test", "x", "y", "z", "raw"],
        "DEFAULT": ["timestamp", "result", "command", "status", "test", "val1", "raw"]
    }

    timeout_row_map = {
        "READ_WHOAMI": [precise_time, "FAIL", cmd, "TIMEOUT", "ERR", "N/A", "NO_DATA"],
        "READ_ACCEL": [precise_time, "FAIL", cmd, "TIMEOUT", "ERR", "N/A", "N/A", "N/A", "NO_DATA"],
        "DEFAULT": [precise_time, "FAIL", cmd, "TIMEOUT", "ERR", "N/A", "NO_DATA"]
    }

    with open(file_name, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(header_map.get(cmd, header_map["DEFAULT"]))

        if not data:
            print(f"Hardware Timeout: {cmd} failed.")
            writer.writerow(timeout_row_map.get(cmd, timeout_row_map["DEFAULT"]))
            return

        separated_data: list[str] = data.split(":")
        evaluated_res: str = evaluate_result(separated_data)
        final_format: list[str] = [precise_time, evaluated_res, cmd] + separated_data + [data]

        print(final_format)
        writer.writerow(final_format)