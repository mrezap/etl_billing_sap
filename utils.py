import os
import calendar
import time
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from config import INPUT_XL_PATH

MONTHS_ABBR = {
    1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MEI", 6: "JUN",
    7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"
}

def month_name(m):
    return f" - {MONTHS_ABBR.get(m, 'UNKNOWN')}"

def get_input_folder():
    check_date = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))
    ym = check_date.strftime("%y%m")
    suffix = month_name(check_date.month)
    fd_path = os.path.join(INPUT_XL_PATH, str(check_date.year), ym + suffix)
    return fd_path

def get_valid_input_folder():
    dt_now = datetime.now()
    for offset in range(0, 2):  # cek bulan sekarang + 1 bulan sebelumnya
        check_date = dt_now - relativedelta(months=offset)
        ym = check_date.strftime("%y%m")
        suffix = month_name(check_date.month)
        fd_path = os.path.join(INPUT_XL_PATH, str(check_date.year), ym + suffix)
        if os.path.exists(fd_path):
            return fd_path
    return None

def is_temp_file(path):
    return os.path.basename(path).startswith("~$")

def wait_for_file_ready(file_path, retries=10, delay=5):
    for _ in range(retries):
        try:
            with open(file_path, "r"):
                return True
        except PermissionError:
            time.sleep(delay)
    return False

def convert_serial_date(v):
    if isinstance(v, int) and v>365:
        return (datetime(1899,12,30)+timedelta(days=v)).strftime("%Y-%m-%d")
    return v