import os
import pandas as pd
from queue import Queue
from threading import Event
from db import engine, column_set, sp_name
from logger import logger
from utils import wait_for_file_ready, convert_serial_date
from config import OUTPUT_CSV_PATH
from refresher import run_refresh_pbi

file_queue     = Queue()
running        = True
task_complete  = Event()
task_complete.set()
file_count     = 0

def process_excel_file():
    global running, file_count
    while running:
        path = file_queue.get()
        if path is None:
            logger.warning("Queue received stop signal!")
            break
        task_complete.clear()
        file_count+=1
        logger.info("Starting a Task....")

        if not wait_for_file_ready(path):
            logger.error(f"File not ready in: {path}")
            task_complete.set()
            continue

        try:
            logger.info(f"Processing file: {path}")
            df = pd.read_excel(path, sheet_name="Sheet1", engine="openpyxl")
            logger.info(f"Reading file: {path} to Pandas")
            df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
            if "Billing Date" in df.columns:
                df["Billing Date"] = df["Billing Date"].apply(convert_serial_date)
        except Exception as e:
            logger.error(f"Error reading file {path}: {e}")
            #return
            task_complete.set()
            continue

        try:
            os.makedirs(OUTPUT_CSV_PATH, exist_ok=True)
            csv_path = os.path.join(
                OUTPUT_CSV_PATH, os.path.basename(path).replace(".xlsx",".csv"))
            df.to_csv(csv_path, index=False)
            logger.info(f"Saved CSV: {os.path.basename(csv_path)}")
        except Exception as e:
            logger.error(f"Error writing CSV for {path}: {e}")
            #return
            task_complete.set()
            continue
        
        # → upload to Postgres
        try:
            #cols = ', '.join([f'"{c}"' for c in df.columns])
            cols = ', '.join(column_set)
            with engine.connect() as conn:
                raw = conn.connection
                cur = raw.cursor()
                with open(csv_path,"r") as f:
                    cur.execute(f"CREATE TEMP TABLE stg_billing (LIKE landing.raw_billing_sap INCLUDING ALL) ON COMMIT DROP")
                    logger.info(f"Temp table has been created!")
                    cur.copy_expert(f"COPY stg_billing ({cols}) FROM STDIN WITH CSV HEADER", f)
                    logger.info(f"Data inserted to temp table!")
                    cur.execute(f"CALL {sp_name}()")
                    raw.commit()
                    logger.info(f"Stored Procedure {sp_name} successfully run!")
                cur.close()
            logger.info(f"Imported to Postgres: {os.path.basename(csv_path)}")
        except Exception as e:
            logger.error(f"Db PostgresSQL error: {e}")
            cur.close()
            raw.close()

        file_queue.task_done()
        logger.info(f"Queue file after processing: {file_queue.qsize()}")
        logger.info(f"Task Done! Total processed: {file_count} file")
        task_complete.set()

        if file_queue.empty():
            file_count = 0
            run_refresh_pbi(logger)