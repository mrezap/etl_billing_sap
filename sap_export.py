import win32com.client
import time
import os
import shutil
import psutil
from datetime import datetime, timedelta
from utils import get_valid_input_folder
#from logger import logger

def is_excel_file_open(target_file):
    try:
        excel = win32com.client.GetActiveObject("Excel.Application")
        for wb in excel.Workbooks:
            if wb.Name.lower() == target_file.lower():
                return wb
    except Exception:
        return None

day_min_1 = (datetime.today() - timedelta(days=1)).strftime("%d.%m.%Y") #recheck
temp_folder = fr"C:\Users\maulana.pahlevi\Documents\SAP\SAP GUI"
site_code_folder = fr"D:\CM Sharing Folder\@Database"
site_code_file = "site_code_sap.txt"
final_folder = get_valid_input_folder()\
#final_folder = fr"D:\CM Sharing Folder\Playground\Output" # for local testing
export_filename = "BILLING SAP TEMP.xlsx"
final_filename = f"BILLING SAP {(datetime.today() - timedelta(days=1)).strftime('%d %B %Y').upper()}.xlsx"

SapGuiAuto = win32com.client.GetObject("SAPGUI")
application = SapGuiAuto.GetScriptingEngine
connection = application.Children(0)
session = connection.Children(0)

session.findById("wnd[0]").maximize()
session.findById("wnd[0]/usr/ctxtS_VKORG-LOW").text = "1010"
session.findById("wnd[0]/usr/ctxtS_VTWEG-LOW").text = "20"
session.findById("wnd[0]/usr/btn%_S_WERKS_%_APP_%-VALU_PUSH").press()
time.sleep(3)
#session.findById("wnd[1]/tbar[0]/btn[24]").press()
session.findById("wnd[1]/tbar[0]/btn[23]").press()
session.findById("wnd[2]/usr/ctxtDY_PATH").text = site_code_folder
session.findById("wnd[2]/usr/ctxtDY_FILENAME").text = site_code_file
session.findById("wnd[2]/tbar[0]/btn[0]").press()
time.sleep(2)
session.findById("wnd[1]/tbar[0]/btn[8]").press()
session.findById("wnd[0]/usr/ctxtS_FKDAT-LOW").text = day_min_1
session.findById("wnd[0]/tbar[1]/btn[8]").press()
#time.sleep(600)
session.findById("wnd[0]").maximize()

#element_path = "wnd[0]/usr/cntlGRID1/shellcont/shell/shellcont[1]/shell"
element_path = "wnd[0]/tbar[1]/btn[43]"

timeout = 720
start_time = time.time()
while True:
    try:
        element = session.FindById(element_path, False)
        if element is not None:
            print("Elemen ditemukan!")
            #session.FindById("wnd[0]").SendVKey(43)
            session.findById("wnd[0]/tbar[1]/btn[43]").press()
            #session.findById("wnd[0]/mbar/menu[0]/menu[1]/menu[1]").select()
            break
    except Exception:
        pass

    if time.time() - start_time > timeout:
        print("Timeout: elemen tidak muncul.")
        break

    time.sleep(60)  # Cek setiap 1 menit

time.sleep(5)
session.findById("wnd[1]/usr/ctxtDY_PATH").text = final_folder
session.findById("wnd[1]/usr/ctxtDY_FILENAME").text =final_filename
#session.findById("wnd[1]/tbar[0]/btn[0]").press()
session.findById("wnd[1]/tbar[0]/btn[11]").press() #replace
time.sleep(5)

# timeout = 10
# elapsed = 0
# while not os.path.exists(temp_folder) and elapsed < timeout:
#     time.sleep(1)
#     elapsed += 1

# time.sleep(5)

# wb = is_excel_file_open(export_filename)

# if wb:
#     wb.Close(SaveChanges=False)
#     time.sleep(5)
#     print("Workbook berhasil ditutup via Excel COM.")
# else:
#     print("Excel tidak sedang membuka file tersebut.")

# temp_files = os.listdir(temp_folder)
# for file in temp_files:
#     file_path = os.path.join(temp_folder, file)
#     if file.startswith("~$"):
#         if os.access(file_path, os.W_OK):
#             os.remove(file_path)
#             print(f"File temp {file} dihapus.")
#         else:
#             print(f"File {file} masih locking")

# try:
#     excel_app = win32com.client.GetActiveObject("Excel.Application")
#     if excel_app.Workbooks.Count == 0:
#         for proc in psutil.process_iter(['name']):
#             if 'EXCEL.EXE' in proc.info['name']:
#                 proc.terminate()
#                 time.sleep(5)
#                 print("Proses EXCEL.EXE dihentikan.")
# except Exception:
#     print("Excel COM tidak tersedia, lanjut ke terminate EXCEL.EXE manual.")

# source_file = os.path.join(temp_folder, export_filename)
# destination_file = os.path.join(final_folder, final_filename)

# if os.path.exists(source_file):
#     shutil.move(source_file, destination_file)
#     print(f"File berhasil dipindah ke: {destination_file}")
# else:
#     print("File tidak ditemukan setelah export, cek SAP atau path.")
