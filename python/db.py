import mysql.connector
from mysql.connector import Error
import os
import sys
from dotenv import load_dotenv


def get_base_path():
    if getattr(sys, '_MEIPASS', None):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(get_base_path(), ".env"))

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "sales")
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Fail to connect MySQL: {e}")
        return None