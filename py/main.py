import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Importing your existing backend modules
import crud_customers as customer_db
import crud_products as product_db
import crud_orders as order_db
import crud_inventory as inventory_db
import reports as report_db

# --- CONFIGURATION & STYLING ---
COLORS = {
    "bg": "#121212",
    "sidebar": "#1E1E1E",
    "mint": "#98FFD2",
    "orange": "#EE4D2D",
    "text": "#FFFFFF",
    "gray": "#2D2D2D"
}

class SalesApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sales Pro - Management System")
        self.geometry("1300x850")
        self.configure(fg_color=COLORS["bg"])
        
        # UI State
        self.current_frame = None
        self.setup_sidebar()
        self.show_dashboard() # Initial View

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COLORS["sidebar"])
        self.sidebar.pack(side="left", fill="y")

        self.logo = ctk.CTkLabel(self.sidebar, text="SALES PRO", 
                                font=("League Spartan", 28, "bold"), text_color=COLORS["mint"])
        self.logo.pack(pady=40)

        # Navigation Buttons
        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Customers", self.show_customers),
            ("Inventory", self.show_products),
            ("Orders", self.show_orders),
            ("Reports", self.show_reports)
        ]

        for text, cmd in nav_items:
            btn = ctk.CTkButton(self.sidebar, text=text, command=cmd, 
                                fg_color="transparent", text_color=COLORS["text"],
                                hover_color=COLORS["orange"], font=("League Spartan", 16),
                                anchor="w", height=45)
            btn.pack(fill="x", padx=20, pady=5)

    def clear_container(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.current_frame.pack(side="right", fill="both", expand=True, padx=30, pady=30)

    # --- DASHBOARD MODULE ---
    def show_dashboard(self):
        self.clear_container()
        lbl = ctk.CTkLabel(self.current_frame, text="Performance Dashboard", font=("League Spartan", 24, "bold"))
        lbl.pack(anchor="w", pady=(0, 20))

        # Metric Cards
        card_container = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        card_container.pack(fill="x")

        # Pulling data from your existing reports.py logic
        low_stock_count = len(inventory_db.get_low_stock(10))
        
        self.create_card(card_container, "Low Stock Alerts", str(low_stock_count), "#FF4D4D")
        self.create_card(card_container, "System Status", "Connected", COLORS["mint"])

    def create_card(self, master, title, value, color):
        card = ctk.CTkFrame(master, fg_color=COLORS["gray"], border_width=1, border_color=color, width=250, height=150)
        card.pack(side="left", padx=10, expand=True)
        ctk.CTkLabel(card, text=title, font=("League Spartan", 14)).pack(pady=(20, 5))
        ctk.CTkLabel(card, text=value, font=("League Spartan", 32, "bold"), text_color=color).pack(pady=10)

    # --- CUSTOMER MANAGEMENT MODULE ---
    def show_customers(self):
        self.clear_container()
        
        # Header with Search Bar
        search_frame = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 20))
        
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Search Name or Phone...", 
                                    width=400, font=("League Spartan", 14))
        search_entry.pack(side="left")
        
        def run_search():
            data = customer_db.search_customer(search_entry.get())
            self.update_tree(tree, data)

        ctk.CTkButton(search_frame, text="Search", width=100, fg_color=COLORS["orange"], command=run_search).pack(side="left", padx=10)

        # Table Section
        tree = self.create_styled_tree(self.current_frame, ["ID", "Name", "Address", "Phone"])
        
        # Load Data using your backend
        initial_data = customer_db.get_all_customers()
        self.update_tree(tree, initial_data)

    def create_styled_tree(self, master, cols):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=COLORS["gray"], foreground="white", fieldbackground=COLORS["gray"], borderwidth=0, font=("Arial", 11))
        style.map("Treeview", background=[('selected', COLORS["orange"])])
        
        tree = ttk.Treeview(master, columns=cols, show="headings", height=15)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill="both", expand=True)
        return tree

    def update_tree(self, tree, data):
        tree.delete(*tree.get_children())
        for row in data:
            # Map dictionary keys to column order
            tree.insert("", "end", values=(row['CustomerID'], row['CustomerName'], row['Address'], row['PhoneNumber']))

    # --- ORDER MANAGEMENT (TRADITIONAL TRIGGER INTEGRATION) ---
    def show_orders(self):
        self.clear_container()
        
        # Load orders and highlight Completed ones
        orders = order_db.get_all_orders()
        
        tree = self.create_styled_tree(self.current_frame, ["OrderID", "Customer", "Date", "Status"])
        tree.tag_configure("Completed", foreground=COLORS["mint"])
        tree.tag_configure("Pending", foreground=COLORS["orange"])
        tree.tag_configure("Cancelled", foreground="gray")

        for o in orders:
            tree.insert("", "end", values=(o['OrderID'], o['CustomerName'], o['OrderDate'], o['Status']), tags=(o['Status'],))

        # Bottom Actions
        act_frame = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        act_frame.pack(fill="x", pady=20)

        def handle_cancel():
            selected = tree.selection()
            if selected:
                oid = tree.item(selected[0])['values'][0]
                if messagebox.askyesno("Confirm", f"Cancel Order #{oid}? Triggers will restore stock."):
                    try:
                        order_db.cancel_order(oid) # Triggers in DB handle stock
                        self.show_orders()
                    except Exception as e:
                        messagebox.showerror("DB Error", str(e))

        ctk.CTkButton(act_frame, text="Cancel Selected Order", fg_color="#444", command=handle_cancel).pack(side="right")

if __name__ == "__main__":
    app = SalesApp()
    app.mainloop()