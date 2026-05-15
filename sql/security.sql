CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin2006@';
CREATE USER 'staff'@'localhost' IDENTIFIED BY 'staff123@';
CREATE USER 'viewer'@'localhost' IDENTIFIED BY 'view1234@';


CREATE ROLE 'admin_role';
CREATE ROLE 'staff_role';
CREATE ROLE 'viewer_role';

GRANT ALL PRIVILEGES ON sales.* TO 'admin_role';

GRANT SELECT, INSERT, UPDATE ON sales.orders TO 'staff_role';
GRANT SELECT, INSERT ON sales.orderdetails TO 'staff_role';
GRANT SELECT ON sales.products TO 'staff_role';

GRANT SELECT ON sales.* TO 'viewer_role';

GRANT 'admin_role' TO 'admin'@'localhost';
GRANT 'staff_role' TO 'staff'@'localhost';
GRANT 'viewer_role' TO 'viewer'@'localhost';

SET DEFAULT ROLE ALL TO 'admin'@'localhost';
SET DEFAULT ROLE ALL TO 'staff'@'localhost';
SET DEFAULT ROLE ALL TO 'viewer'@'localhost';

FLUSH PRIVILEGES;

-- Backup 