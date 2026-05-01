import csv
import os
from datetime import datetime

from analyzer import evaluate_result
from config import DATA_DIR_NAME
from serial_comm import send_command


def get_precise_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def get_data_dir() -> str:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, DATA_DIR_NAME)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_csv_header(cmd: str) -> list[str]:
    header_map = {
        "READ_WHOAMI": ["timestamp", "result", "command", "status", "device_command", "test", "val", "raw"],
        "READ_ACCEL": ["timestamp", "result", "command", "status", "device_command", "test", "x", "y", "z", "raw"],
        "READ_WHOAMI_BAD_ADDR": ["timestamp", "result", "command", "status", "device_command", "reason", "raw"],
        "DEFAULT": ["timestamp", "result", "command", "status", "device_command", "value", "raw"]
    }
    return header_map.get(cmd, header_map["DEFAULT"])


def build_csv_row(cmd: str, response: str, result: str) -> list[str]:
    timestamp = get_precise_time()

    if not response:
        timeout_rows = {
            "READ_WHOAMI": [timestamp, "FAIL", cmd, "TIMEOUT", cmd, "ERR", "N/A", "NO_DATA"],
            "READ_ACCEL": [timestamp, "FAIL", cmd, "TIMEOUT", cmd, "ERR", "N/A", "N/A", "N/A", "NO_DATA"],
            "READ_WHOAMI_BAD_ADDR": [timestamp, "FAIL", cmd, "TIMEOUT", cmd, "NO_DATA", "NO_DATA"],
            "DEFAULT": [timestamp, "FAIL", cmd, "TIMEOUT", cmd, "NO_DATA", "NO_DATA"]
        }
        return timeout_rows.get(cmd, timeout_rows["DEFAULT"])

    fields = response.split(":")
    return [timestamp, result, cmd] + fields + [response]


def write_result_csv(cmd: str, response: str, result: str) -> None:
    data_dir = get_data_dir()
    file_name = os.path.join(data_dir, f"test_{cmd}.csv")
    file_exists = os.path.isfile(file_name)

    with open(file_name, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(get_csv_header(cmd))

        writer.writerow(build_csv_row(cmd, response, result))


def send_command_csv(ser, cmd: str) -> str:
    response = send_command(ser, cmd)

    if ":" in response:
        result = evaluate_result(response.split(":"))
    elif response in ("PASS", "FAIL"):
        result = response
    else:
        result = "FAIL"

    write_result_csv(cmd, response, result)
    return result