import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

# Define Path
INPUT_XL_PATH = os.getenv("INPUT_XL_PATH")
OUTPUT_CSV_PATH = os.getenv("OUTPUT_CSV_PATH")
LOG_FILE = os.getenv("LOG_FILE")

# DB Cred & Conn
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", ""))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# PBI API
PBI_SCRIPTS = os.getenv("PBI_SCRIPTS","").split(";")