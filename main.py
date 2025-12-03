import time
from threading import Thread
from watchdog.observers import Observer
from utils import get_valid_input_folder
from handler import ExcelHandler
from processor import process_excel_file, file_queue
from logger import logger

def main():
    # worker
    worker = Thread(target=process_excel_file, daemon=True)
    worker.start()

    curr_folder = get_valid_input_folder()
    if not curr_folder:
        logger.info(f"Cannot find a spesific folder")
        exit()

    watcher = Observer(timeout=10)
    watcher.schedule(ExcelHandler(), path=curr_folder, recursive=False)
    watcher.start()
    logger.info(f"Observing: {curr_folder}")

    try:
        while True:
            time.sleep(60)
            newf = get_valid_input_folder()
            if newf != curr_folder:
                logger.info(f"Folder change: {curr_folder} → {newf}. Restarting observer")
                watcher.stop(); watcher.join()
                curr_folder = newf
                logger.info(f"Starting observer on folder: {curr_folder}")
                watcher = Observer(timeout=10)
                watcher.schedule(ExcelHandler(), path=curr_folder, recursive=False)
                watcher.start()
            logger.info("Watching for new files…")
    except KeyboardInterrupt:
        running=False
        watcher.stop()
        file_queue.put(None)
        logger.info("Shutdown requested")
    except Exception as e:
        watcher.stop()
        time.sleep(30)
        logger.error(f"An unexpected error occurred: {e}")
        logger.info("Watching for new files was stopped")
    finally:
        watcher.stop()
        file_queue.put(None)
        worker.join()

if __name__ == "__main__":
    main()