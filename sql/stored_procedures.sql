DELIMITER //
CREATE PROCEDURE create_order(IN p_customer_id INT, IN p_employee_id INT)
BEGIN
    INSERT INTO orders (customerid, employeeid, orderdate, status)
    VALUES (p_customer_id, p_employee_id, CURDATE(), 'Pending');
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE add_order_detail(
    IN p_order_id INT,
    IN p_product_id INT,
    IN p_quantity INT,
    IN p_price DECIMAL(10,2)
)
BEGIN
    INSERT INTO orderdetails (orderid, productid, quantity, saleprice)
    VALUES (p_order_id, p_product_id, p_quantity, p_price);
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE cancel_order(IN p_order_id INT)
BEGIN
    UPDATE orders
    SET status = 'Cancelled'
    WHERE orderid = p_order_id
    AND status <> 'Cancelled';
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE complete_order(IN p_order_id INT)
BEGIN
    UPDATE orders
    SET status = 'Completed'
    WHERE orderid = p_order_id
    AND status = 'Pending';
END //

DELIMITER ;