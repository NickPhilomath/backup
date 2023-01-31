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