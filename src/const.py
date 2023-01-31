import os
from dotenv import load_dotenv

load_dotenv()

HOST = 'localhost'
DATABASE_NAME = 'backup'
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASS = os.getenv('MYSQL_PASSWORD')