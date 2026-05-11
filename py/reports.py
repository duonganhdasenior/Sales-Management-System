from db import get_connection
def get_report(view_name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"SELECT * FROM {view_name}")
    data = cursor.fetchall()

    conn.close()
    return data

