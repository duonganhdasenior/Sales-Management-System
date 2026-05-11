from db import get_connection
def get_report(view_name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"SELECT * FROM {view_name}")
    data = cursor.fetchall()

    conn.close()
    return data

def report_menu():
    while True:
        print("\n--- REPORT MENU ---")
        print("1. Daily Sales")
        print("2. Monthly Sales")
        print("3. Top Products")
        print("4. Customer Revenue")
        print("5. Inventory Value")
        print("6. Low Stock")
        print("7. Pending Orders")
        print("8. Today Pending Orders")
        print("9. Orders with Customers")
        print("10. Delivery Success Rate")
        print("0. Exit")

        choice = input("Choose: ")

        views = {
            "1": "vw_daily_sales",
            "2": "vw_sales_per_month",
            "3": "vw_top_products",
            "4": "vw_customer_rev",
            "5": "vw_inventory_value",
            "6": "vw_low_stock",
            "7": "vw_pending_orders",
            "8": "vw_pending_orders_today",
            "9": "vw_orders_with_customers",
            "10": "vw_deli_success_rate"
        }

        if choice == "0":
            break
        elif choice in views:
            data = get_report(views[choice])
            for row in data:
                print(row)