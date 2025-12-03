import os, time
import threading
from watchdog.events import FileSystemEventHandler
from utils import is_temp_file
from processor import file_queue, task_complete
from logger import logger

def is_file_ready(path, interval=0.5, retries=3):
    last_size = -1
    for _ in range(retries):
        try:
            size = os.path.getsize(path)
            if size == last_size:
                return True
            last_size = size
            time.sleep(interval)
        except FileNotFoundError:
            return False
    return False

class ExcelHandler(FileSystemEventHandler):
    def __init__(self, delay=5):
        super().__init__()
        self.delay = delay
        self.buf   = []
        self.lock  = threading.Lock()
        self.timer = None

    def on_created(self, event):
        logger.info(f"CREATED: {event.src_path}")
        if event.src_path.lower().endswith(".xlsx") and not is_temp_file(event.src_path):
            logger.info(f"File accepted: {event.src_path}")
            try: os.chmod(event.src_path, 0o666)
            except PermissionError:
                logger.error(f"Permission denied: {event.src_path}")

            with self.lock:
                self.buf.append(event.src_path) 
                logger.info(f"Buffered: {event.src_path}")
                if not self.timer or not self.timer.is_alive():
                    self.timer = threading.Timer(self.delay, self.flush)
                    self.timer.start()
        else:
            logger.warning(f"File rejected: {event.src_path}")

    def flush(self):
        with self.lock:
            files = self.buf.copy(); self.buf.clear()
        logger.info("New files added: " + ", ".join(files))
        for f in files:
            if is_file_ready(f):
                task_complete.wait()
                file_queue.put(f)
                logger.info(f"Queued: {f}")
            else:
                logger.warning(f"Skipped (not ready): {f}")
        logger.info(f"Queue size: {file_queue.qsize()}")

