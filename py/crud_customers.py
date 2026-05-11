from db import get_connection

def add_customer(name, address, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Customers (CustomerName, Address, PhoneNumber)
        VALUES (%s, %s, %s)
    """, (name, address, phone))
    conn.commit()
    conn.close()

def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Customers")
    data = cursor.fetchall()
    conn.close()
    return data

def get_customer_by_id(customer_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Customers WHERE CustomerID=%s", (customer_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def search_customer(query_str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
   
    query = """
        SELECT * FROM Customers 
        WHERE CustomerName LIKE %s OR PhoneNumber LIKE %s
    """
    search_term = f"%{query_str}%"
    cursor.execute(query, (search_term, search_term))
    results = cursor.fetchall()
    conn.close()
    return results

def get_customer_order_history(customer_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT o.OrderID, o.OrderDate, o.Status, 
               SUM(od.Quantity * od.SalePrice) as TotalAmount
        FROM Orders o
        LEFT JOIN OrderDetails od ON o.OrderID = od.OrderID
        WHERE o.CustomerID = %s
        GROUP BY o.OrderID
        ORDER BY o.OrderDate DESC
    """
    cursor.execute(query, (customer_id,))
    history = cursor.fetchall()
    conn.close()
    return history

def update_customer(customer_id, name, address, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Customers
        SET CustomerName=%s, Address=%s, PhoneNumber=%s
        WHERE CustomerID=%s
    """, (name, address, phone, customer_id))
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Customers WHERE CustomerID=%s", (customer_id,))
    conn.commit()
    conn.close()