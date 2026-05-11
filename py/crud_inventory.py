
from db import get_connection

def check_stock(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT StockQuantity FROM Products WHERE ProductID=%s", (product_id,))
    stock = cursor.fetchone()
    conn.close()
    return stock[0] if stock else None


def restock(product_id, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Products
        SET StockQuantity = StockQuantity + %s
        WHERE ProductID = %s
    """, (quantity, product_id))
    conn.commit()
    conn.close()


def get_low_stock(threshold=10):
    """Trả về danh sách sản phẩm có tồn kho dưới ngưỡng threshold (mặc định < 10)"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ProductID, ProductName, StockQuantity
        FROM Products
        WHERE StockQuantity < %s
        ORDER BY StockQuantity ASC
    """, (threshold,))
    data = cursor.fetchall()
    conn.close()
    return data