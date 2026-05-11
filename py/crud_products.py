from db import get_connection
def add_product(name, price, stock):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO Products (ProductName, Price, StockQuantity)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (name, price, stock))

    conn.commit()
    conn.close()

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Products")
    data = cursor.fetchall()
    conn.close()
    return data

def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Products WHERE ProductID = %s", (product_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def search_product_by_name(name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # Sử dụng CONCAT để kết hợp dấu % với tham số đầu vào một cách an toàn
    query = "SELECT * FROM Products WHERE ProductName LIKE %s"
    search_term = f"%{name}%"
    
    cursor.execute(query, (search_term,))
    results = cursor.fetchall()
    conn.close()
    return results
    
def get_product_sales_count(product_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # SUM(Quantity) để tính tổng số lượng sản phẩm đã xuất kho
    query = """
        SELECT SUM(Quantity) as total_sold 
        FROM OrderDetails 
        WHERE ProductID = %s
    """
    
    cursor.execute(query, (product_id,))
    result = cursor.fetchone()
    conn.close()
    
    # Nếu sản phẩm chưa bao giờ được bán, SUM sẽ là None, ta trả về 0
    return result['total_sold'] if result['total_sold'] is not None else 0

def update_product(product_id, name, price, stock):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Products
        SET ProductName=%s, Price=%s, StockQuantity=%s
        WHERE ProductID=%s
    """, (name, price, stock, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Products WHERE ProductID=%s", (product_id,))
    conn.commit()
    conn.close()