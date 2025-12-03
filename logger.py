import os, logging
from config import LOG_FILE

def write_log_header(log_file):
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("Timestamp,Level,Message\n")

def get_logger():
    write_log_header(LOG_FILE)
    logger = logging.getLogger("CSVLogger")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(LOG_FILE, mode="a")
    fmt = logging.Formatter("%(asctime)s,%(levelname)s,\"%(message)s\"", 
                            datefmt="%Y-%m-%d %H:%M:%S")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    return logger

logger = get_logger()