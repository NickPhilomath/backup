import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

HOST = 'localhost'
DATABASE_NAME = 'backup'
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASS = os.getenv('MYSQL_PASSWORD')

BASE_DIR = Path(__file__).resolve().parent.parent
BACKUP_DIR = os.path.join(BASE_DIR, 'backup')

"""
get_file()
Use this method to get basic information about a file and prepare it for downloading. 
For the moment, bots can download files of up to 20MB in size. On success, a File object is returned. 
The file can then be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>, where <file_path> is taken from the response. 
It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling getFile again
"""
DOWNLOAD_LIMIT = 20000000
TELEGRAM_DOWNLOAD_URL = 'https://api.telegram.org/file/bot'