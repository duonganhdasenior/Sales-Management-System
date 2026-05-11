DELIMITER //

CREATE TRIGGER trg_after_insert_orderdetails
AFTER INSERT ON orderdetails
FOR EACH ROW
BEGIN
    IF NEW.quantity > 0 THEN
        UPDATE products
        SET stockquantity = stockquantity - NEW.quantity
        WHERE productid = NEW.productid;
    END IF;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER trg_before_insert_orderdetails
BEFORE INSERT ON orderdetails
FOR EACH ROW
BEGIN
    DECLARE v_stock INT;

    SELECT stockquantity INTO v_stock
    FROM products
    WHERE productid = NEW.productid;

    IF v_stock IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Product does not exist !';
    END IF;

    IF v_stock < NEW.quantity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Not enough stock!!';
    END IF;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER trg_after_update_orders
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    IF NEW.status = 'Cancelled' AND OLD.status <> 'Cancelled' THEN

        UPDATE products p
        JOIN orderdetails od ON p.productid = od.productid
        SET p.stockquantity = p.stockquantity + od.quantity
        WHERE od.orderid = NEW.orderid;

    END IF;
END //

DELIMITER ;