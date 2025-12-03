import os
import shutil
from datetime import datetime, timedelta
from utils import get_valid_input_folder
#from logger import logger

source_folder = get_valid_input_folder()
destination_folder = fr"D:\CM Sharing Folder\@Database\Gdrive Share Folder\Billing TAM Channel 20"
export_filename = "BILLING SAP TEMP.xlsx"
final_filename = f"BILLING SAP {(datetime.today() - timedelta(days=1)).strftime('%d %B %Y').upper()}.xlsx"

# Get all file in source folder
files = [os.path.join(source_folder, f) for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

# Find latest modified time
latest_file = max(files, key=os.path.getmtime)
filename = os.path.basename(latest_file)

# Copy file
destination_path = os.path.join(destination_folder, final_filename)
shutil.copy2(latest_file, destination_path)

print(f"File terbaru berhasil dicopy ke: {destination_path}")