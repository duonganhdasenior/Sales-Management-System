from db import get_connection

def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # Lấy danh sách nhân viên để đổ vào Combobox khi tạo đơn hàng
    cursor.execute("SELECT EmployeeID, EmployeeName, JobTitle FROM employees")
    data = cursor.fetchall()
    conn.close()
    return data

def get_employee_by_id(employee_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees WHERE EmployeeID=%s", (employee_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_orders_by_employee(employee_id):
    """Xem danh sách các đơn hàng do một nhân viên cụ thể phụ trách"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT o.OrderID, o.OrderDate, o.Status, c.CustomerName
        FROM Orders o
        JOIN Customers c ON o.CustomerID = c.CustomerID
        WHERE o.EmployeeID = %s
    """
    cursor.execute(query, (employee_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders