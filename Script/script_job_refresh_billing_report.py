import os
import msal
import requests
import json
import pandas as pd
import logging

# ===================#
# Logging Config #
# ===================#
LOG_FILE = r"D:\CM Sharing Folder\Playground\Log\ingest_billing_sap.txt"  # Set log file path
# LOG_FILE = r"Z:\Playground\Log\ingest_billing_sap.txt"  # testing

def write_log_header(log_file):
    try:
        if not os.path.exists(log_file):
            with open(log_file, "w") as f:
                # header_line = "+" + "-" * 21 + "+" + "-" * 10 + "+" + "-" * 65 + "+"
                # header_titles = "| {0:19s} | {1:8s} | {2:63s} |".format("Timestamp", "Level", "Message")
                # f.write(header_line + "\n")
                # f.write(header_titles + "\n")
                # f.write(header_line + "\n")
                f.write("Timestamp","Level","Message\n")
        else:
            pass
    except Exception as e:
        print("Failed to write header to log:", e)

def setup_custom_logger(log_file):
    write_log_header(log_file)
    
    #logger = logging.getLogger("TableLogger")
    logger = logging.getLogger("CSVLogger")
    logger.setLevel(logging.DEBUG)
    
    # Handler untuk menulis ke file
    file_handler = logging.FileHandler(log_file, mode="a")
    # Buat custom formatter: lebar kolom fixed
    #formatter = logging.Formatter("| %(asctime)-19s | %(levelname)-8s | %(message)-65s |", datefmt="%Y-%m-%d %H:%M:%S")
    formatter = logging.Formatter("%(asctime)s,%(levelname)s,\"%(message)s\"", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger

# Setup custom logger dan gunakan variabel 'logger'
logger = setup_custom_logger(LOG_FILE)

# ===================#
# PBI Config Param #
# ===================#

client_id = "26fd9846-9c01-45c2-b3f0-75f746475010" # Service Principal
client_secret = "S2L8Q~dkhYRTzmyEBD8IB9~6D61XjzsnGaD3mbJn"
tenant_id = "578dbadd-c32c-4f5a-8c44-33da44c71209" 
workspace_id = "1fa42805-42c8-49e3-ad4d-f54fbd1a4f57" # Check workspace
dataset_id = "d0636919-44b5-4334-b36c-bdd686192191" # Check semantic model

authority_url = "https://login.microsoftonline.com/" + tenant_id 
scope = ["https://analysis.windows.net/powerbi/api/.default"]
url = "https://api.powerbi.com/v1.0/myorg/groups/" + workspace_id +"/datasets/"+ dataset_id +"/refreshes?$top=1"


# ===================#
# Token Auth #
# ===================#
app = msal.ConfidentialClientApplication(client_id, authority=authority_url, client_credential=client_secret)
result = app.acquire_token_for_client(scopes=scope)

#print(json.dumps(result, indent=2)) #debugging token


#Get latest Power BI Dataset Refresh
if 'access_token' in result:
    access_token = result['access_token']
    header = {'Content-Type':'application/json', 'Authorization':f'Bearer {access_token}'}
    api_call = requests.get(url=url, headers=header)

    result = api_call.json()['value']
    
    df = pd.DataFrame(result, columns=['requestId', 'id', 'refreshType', 'startTime', 'endTime', 'status'])
    df.set_index('id')

if df.status[0] == "Unknown":
    logger.info("Semantic Model: Billing Report - Dataset is refreshing right now. Please wait until this refresh has finished to trigger a new one.")
elif df.status[0] == "Disabled":
    logger.error("Semantic Model: Billing Report - Dataset refresh is disabled. Please enable it.")
elif df.status[0] == "Failed":
    logger.warning("Semantic Model: Billing Report - Last Dataset refresh failed. Please check error message.")
elif df.status[0] == "Completed":
    api_call = requests.post(url=url, headers=header)
    logger.info("Semantic Model: Billing Report - Triggered a Dataset refresh.")
else:
    logger.warning("Not familiar with status, please check documentatino for status: '" + df.status[0] + "'")