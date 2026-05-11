-- Tạo index để truy xuất nhanh hơn
CREATE INDEX idx_customer_name ON Customers(CustomerName);
CREATE INDEX idx_product_name ON Products(ProductName);
CREATE INDEX idx_order_date ON Orders(OrderDate);
CREATE INDEX idx_order_status ON Orders(Status);
CREATE INDEX idx_employee_job ON Employees(JobTitle);
CREATE INDEX idx_order_customer ON Orders(CustomerID);
CREATE INDEX idx_order_employee ON Orders(EmployeeID);

-- Tạo views 
-- Daily orders: total orders per day 
create or replace view vw_daily_orders as
select OrderDate, count(*) as total_orders
from orders
group by OrderDate;

-- orders_with_customers: in4 khách hàng & their orders
create or replace view vw_orders_with_customers AS
select o.OrderID, c.CustomerName, o.OrderDate, o.Status
from orders o
join customers c on o.CustomerID = c.CustomerID;

-- Daily Sales: total sales per day 
create or replace view vw_daily_sales as
select OrderDate, SUM(Quantity*SalePrice) as Revenue
from Orders o
join OrderDetails od on o.OrderID = od.OrderID
group by OrderDate;

-- Sales per Product
create or replace view vw_sales_per_product as
select p.ProductID, ProductName, SUM(Quantity) AS Total_sold, SUM(Quantity*SalePrice) as Revenue
from products p 
join orderdetails od on p.ProductID = od.ProductID
group by p.ProductID, ProductName;

-- Top Selling Product 
create or replace view vw_top_products as
select
    p.ProductName,
    SUM(od.Quantity) as total_sold,
    DENSE_RANK() OVER (ORDER BY SUM(od.Quantity) DESC) AS ranking
from OrderDetails od
join Products p ON od.ProductID = p.ProductID
group by  p.ProductName;

-- Sales per Month
create or replace view vw_sales_per_month as
select year(OrderDate) as year, month(OrderDate) as month, SUM(Quantity*SalePrice) as revenue
from orders o 
join orderdetails od 
on o.orderid = od.orderid
group by year, month
order by year, month;

-- Customer Revenue
create or replace view vw_customer_rev as
select customername, SUM(Quantity*SalePrice) as revenue 
from customers c
join orders o on c.customerid = o.customerid
join orderdetails od on o.orderid = od.orderid
group by customername
order by revenue DESC;

-- Low Stock Products
create or replace view vw_low_stock AS
select
    ProductName,
    StockQuantity
from Products
where StockQuantity < 10; 

-- Inventory Value 
create or replace view vw_inventory_value AS
select 
    ProductName,
    StockQuantity,
    Price,
    (StockQuantity * Price) as total_value
from Products;

-- Successful Delivery rate
create or replace view vw_deli_success_rate AS
select 
    COUNT(CASE WHEN Status = 'Completed' THEN 1 END) * 1.0 / COUNT(*) AS success_rate
from Orders;

-- Pending Orders
create or replace view vw_pending_orders AS
select
    o.OrderID, 
    c.CustomerName, 
    c.PhoneNumber, 
    o.OrderDate,
    o.Status
from Orders o
join Customers c ON o.CustomerID = c.CustomerID
where o.Status = 'Pending'
order by o.OrderDate ASC;

-- Today's Pending Orders
create or replace view vw_pending_orders_today AS
select
    o.OrderID,
    c.CustomerName,
    c.PhoneNumber,
    o.OrderDate,
    o.Status
from Orders o
join Customers c ON o.CustomerID = c.CustomerID
where o.Status = 'Pending'
  AND o.OrderDate = CURDATE()
order by o.OrderID ASC;

