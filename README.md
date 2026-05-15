# Sales-Management-System
# SalesPro — Sales Management System

A desktop sales management application built with **Python** and **MySQL** as a Database Management Systems course project at National Economics University (NEU).

---

## Features

| Module | Capabilities |
|---|---|
| **Customers** | Add, edit, delete, search, view purchase history |
| **Products** | Manage catalog, restock, track low stock & sold quantity |
| **Orders** | Create orders, view details, complete or cancel transactions |
| **Employees** | Manage staff profiles and assigned orders |
| **Reports & Dashboard** | Revenue trends, top products, top customers, order status charts |

---

## Database Design

**DBMS:** MySQL 8.4 · **Schema:** 5 normalized tables

```
Customers ──< Orders >── Employees
                │
           OrderDetails >── Products
```

**Advanced objects implemented:**
- 7 performance **Indexes**
- 13 analytical **Views** (daily sales, top products, low stock alerts, etc.)
- 3 **Stored Procedures** (`sp_create_order`, `sp_add_order_detail`, `sp_cancel_order`)
- 5 **User-Defined Functions** (order total, discount tiers, final price, etc.)
- 3 **Triggers** (auto-decrement stock on insert, stock validation before insert, stock restore on cancel)

**Security:** Role-based access control with 3 roles — `admin_role`, `staff_role`, `viewer_role`

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|---|---|---|
| Database | MySQL | 8.4.7 |
| Language | Python | 3.10.11 |
| DB Connector | mysql-connector-python | 9.7.0 |
| GUI | CustomTkinter / Tkinter | Latest |
| Charts | Matplotlib | Latest |
| Packaging | PyInstaller | Latest |

---

## Project Structure

```
sales-pro/
├── main.py                 # GUI entry point
├── db.py                   # MySQL connection factory
├── crud_customers.py
├── crud_products.py
├── crud_orders.py
├── crud_inventory.py
├── crud_employees.py
├── reports.py              # View reader for analytics
├── .env                    # DB credentials (not committed)
└── sql/
    ├── schema_and_seed.sql
    ├── stored_procedures.sql
    ├── triggers.sql
    ├── UDF.sql
    ├── views.sql
    └── security.sql
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- MySQL 8.x running locally

### Installation

```bash
git clone https://github.com/duonganhdasenior/Sales-Management-System.git
cd Sales-Management-System
pip install mysql-connector-python customtkinter matplotlib python-dotenv
```

### Configure Database

1. Run `sql/schema_and_seed.sql` in MySQL Workbench to create and seed the database.
2. Run the remaining SQL files (`stored_procedures.sql`, `triggers.sql`, `UDF.sql`, `views.sql`, `security.sql`).
3. Place the `.env` file in the project root:

```env
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=*password
DB_NAME=sales
```

### Run

```bash
python main.py
```

### Or download the prebuilt executable

 **[Download SalesPro.exe from Releases](../../releases/latest)**

Place `SalesPro.exe` and `.env` in the same folder, then run the `.exe` directly — no Python installation required.

---

##  Demo

 [YouTube Demo](https://www.youtube.com/watch?v=_LfDnxfyvts)

---

## References

- [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Elmasri & Navathe — *Fundamentals of Database Systems*, 7th ed.

---

*National Economics University · DSEB 66B · 2026*
