DELIMITER //

DROP FUNCTION IF EXISTS get_order_total //
CREATE FUNCTION get_order_total(p_order_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10,2);

    SELECT SUM(quantity * saleprice)
    INTO total
    FROM OrderDetails
    WHERE orderid = p_order_id;

    RETURN IFNULL(total, 0);
END //

DELIMITER ;

DELIMITER //
DROP FUNCTION IF EXISTS calculate_discount //
CREATE FUNCTION calculate_discount(total DECIMAL(10,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    RETURN CASE 
        WHEN total >= 100 THEN total * 0.1
        WHEN total >= 50 THEN total * 0.05
        ELSE 0
    END;
END //
DELIMITER ;

DELIMITER //
DROP FUNCTION IF EXISTS get_final_price //
CREATE FUNCTION get_final_price(p_order_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10,2);
    DECLARE discount DECIMAL(10,2);

    SET total = get_order_total(p_order_id);
    SET discount = calculate_discount(total);

    RETURN total - discount;
END //

DELIMITER ;

DELIMITER //
DROP FUNCTION IF EXISTS get_product_revenue //
CREATE FUNCTION get_product_revenue(p_product_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE revenue DECIMAL(10,2);

    SELECT SUM(quantity * saleprice)
    INTO revenue
    FROM orderdetails
    WHERE productid = p_product_id;

    RETURN IFNULL(revenue, 0);
END //

DELIMITER ;

DELIMITER //
DROP FUNCTION IF EXISTS get_success_rate //
CREATE FUNCTION get_success_rate()
RETURNS DECIMAL(5,2)
DETERMINISTIC
BEGIN
    DECLARE rate DECIMAL(5,2);

    SELECT 
        COUNT(CASE WHEN status = 'Completed' THEN 1 END) * 1.0 / COUNT(*)
    INTO rate
    FROM orders;

    RETURN IFNULL(rate, 0);
END //

DELIMITER ;