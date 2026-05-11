import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',        
            password='Anh07102006@', 
            database='sales'   
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Fail to connect MySQL: {e}")
        return None


if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("Connected Successfully!")
        conn.close()