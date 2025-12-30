import os
import shutil
from datetime import datetime, timedelta
from utils import get_valid_input_folder
from logger import logger

source_folder = get_valid_input_folder()
destination_folder = fr"D:\CM Sharing Folder\@Database\Gdrive Share Folder\Billing TAM Channel 20"

target_filename = f"BILLING SAP {(datetime.today() - timedelta(days=1)).strftime('%d %B %Y').upper()}.xlsx"

source_file_path = os.path.join(source_folder, target_filename)

if os.path.exists(source_file_path):
    destination_path = os.path.join(destination_folder, target_filename)
    shutil.copy2(source_file_path, destination_path)
    logger.info(f"File '{target_filename}' berhasil dipindah ke: {destination_path}")
else:
    logger.info(f"File '{target_filename}' tidak ditemukan di folder source")