from db import get_connection


def create_order(customer_id, employee_id, items):
    """
    Tạo đơn hàng mới với danh sách sản phẩm.
    - customer_id : ID khách hàng
    - employee_id : ID nhân viên thực hiện
    - items       : [(product_id, quantity), ...]

    Lưu ý: việc trừ kho được xử lý hoàn toàn bởi trigger
    trg_before_insert_orderdetails (kiểm tra tồn kho) và
    trg_after_insert_orderdetails (trừ kho) — KHÔNG trừ thủ công ở đây.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        conn.start_transaction()

        # 1. Tạo đơn hàng mới với trạng thái Pending
        cursor.execute("""
            INSERT INTO Orders (CustomerID, EmployeeID, OrderDate, Status)
            VALUES (%s, %s, CURDATE(), 'Pending')
        """, (customer_id, employee_id))
        order_id = cursor.lastrowid

        # 2. Chèn từng dòng OrderDetails — trigger sẽ tự kiểm tra & trừ kho
        for product_id, quantity in items:
            # Lấy giá hiện tại của sản phẩm
            cursor.execute(
                "SELECT Price FROM Products WHERE ProductID = %s",
                (product_id,)
            )
            result = cursor.fetchone()

            if not result:
                raise Exception(f"Sản phẩm ID {product_id} không tồn tại.")

            price = result[0]

            # INSERT này kích hoạt trigger kiểm tra & trừ kho tự động
            cursor.execute("""
                INSERT INTO OrderDetails (OrderID, ProductID, Quantity, SalePrice)
                VALUES (%s, %s, %s, %s)
            """, (order_id, product_id, quantity, price))

        conn.commit()
        print(f"Đơn hàng #{order_id} tạo thành công bởi nhân viên #{employee_id}.")
        return order_id

    except Exception as e:
        conn.rollback()
        print("Tạo đơn thất bại:", e)
        raise e  # Re-raise để GUI hiển thị thông báo lỗi

    finally:
        conn.close()


def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            o.OrderID,
            IFNULL(c.CustomerName, '(Khách đã xóa)') AS CustomerName,
            IFNULL(e.EmployeeName, '(NV đã xóa)')    AS EmployeeName,
            o.OrderDate,
            o.Status
        FROM Orders o
        LEFT JOIN Customers c  ON o.CustomerID = c.CustomerID
        LEFT JOIN Employees  e ON o.EmployeeID  = e.EmployeeID
        ORDER BY  o.OrderID ASC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def get_order_by_id(order_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            o.OrderID,
            IFNULL(c.CustomerName, '(Deleted)') AS CustomerName,
            IFNULL(e.EmployeeName, '(Deleted)')    AS EmployeeName,
            o.OrderDate,
            o.Status
        FROM Orders o
        LEFT JOIN Customers c  ON o.CustomerID = c.CustomerID
        LEFT JOIN Employees  e ON o.EmployeeID  = e.EmployeeID
        WHERE o.OrderID = %s
    """, (order_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def get_order_items(order_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            od.ProductID,
            p.ProductName,
            od.Quantity,
            od.SalePrice,
            (od.Quantity * od.SalePrice) AS SubTotal
        FROM OrderDetails od
        JOIN Products p ON od.ProductID = p.ProductID
        WHERE od.OrderID = %s
    """, (order_id,))
    items = cursor.fetchall()
    conn.close()
    return items


def get_order_total(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(Quantity * SalePrice) FROM OrderDetails WHERE OrderID = %s",
        (order_id,)
    )
    total = cursor.fetchone()[0]
    conn.close()
    return float(total) if total else 0.0


def get_order_final_price(order_id):
    """Giá cuối sau giảm giá, dùng UDF get_final_price."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT get_final_price(%s)", (order_id,))
    result = cursor.fetchone()[0]
    conn.close()
    return float(result) if result else 0.0


def update_order_status(order_id, status):
    """Cập nhật trạng thái đơn hàng.
    Trigger trg_after_update_orders tự hoàn kho khi status = 'Cancelled'.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Orders SET Status = %s WHERE OrderID = %s",
        (status, order_id)
    )
    conn.commit()
    conn.close()


def cancel_order(order_id):
    """Hủy đơn hàng.
    Trigger trg_after_update_orders tự hoàn kho — không xử lý thủ công.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        cursor.execute("""
            UPDATE Orders
            SET Status = 'Cancelled'
            WHERE OrderID = %s AND Status <> 'Cancelled'
        """, (order_id,))

        if cursor.rowcount == 0:
            raise Exception(f"Đơn #{order_id} không thể hủy (đã hủy hoặc không tồn tại).")

        conn.commit()
        print(f"Đơn hàng #{order_id} đã hủy. Kho được hoàn lại tự động qua trigger.")

    except Exception as e:
        conn.rollback()
        print("Hủy đơn thất bại:", e)
        raise e

    finally:
        conn.close()


def complete_order(order_id):
    """Chuyển đơn Pending → Completed."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Orders
            SET Status = 'Completed'
            WHERE OrderID = %s AND Status = 'Pending'
        """, (order_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise Exception(f"Đơn #{order_id} không ở trạng thái Pending.")
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
