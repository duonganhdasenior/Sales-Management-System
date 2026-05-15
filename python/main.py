
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

import crud_customers as cust_db
import crud_products  as prod_db
import crud_orders    as ord_db
import crud_inventory as inv_db
import crud_employees as emp_db
import reports        as rep_db
import datetime
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ── Palette ───────────────────────────────────────────────────────────────────
C = {
    "bg"     : "#0F0F0F", "sidebar": "#171717",
    "card"   : "#1E1E1E", "surface": "#252525",
    "border" : "#2E2E2E", "mint"   : "#6EFFC7",
    "mint2"  : "#ADFCDF", "orange" : "#E35F27",
    "orange2": "#FFA894", "text"   : "#F0F0F0",
    "muted"  : "#888888", "green"  : "#00AB06",
    "red"    : "#FF7373", "yellow" : "#FFC107",
    "blue":     "#1b7c8b", "purple":   "#664973",
    "chart_bg": "#1e1e1e",
}
MONTH_LABELS = ["T1","T2","T3","T4","T5","T6","T7","T8","T9","T10","T11","T12"]
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# ═══════════════════════════════════════════════════════════════════════════════
#  TREEVIEW STYLE
# ═══════════════════════════════════════════════════════════════════════════════
def apply_tree_style():
    s = ttk.Style()
    s.theme_use("default")
    s.configure("T.Treeview",
        background=C["surface"], foreground=C["text"],
        fieldbackground=C["surface"], borderwidth=0,bordercolor="#444444",
        rowheight=34, font=("League Spartan", 13))
    s.configure("T.Treeview.Heading",
        background=C["card"], foreground=C["mint"],
        font=("League Spartan", 13, "bold"), relief="flat", borderwidth=0, bordercolor="#FDE8E8")
    s.map("T.Treeview",
        background=[("selected", C["orange"])],
        foreground=[("selected", "#fff")])
    s.layout("T.Treeview", [("T.Treeview.treearea", {"sticky": "nswe"})])


# ═══════════════════════════════════════════════════════════════════════════════
#  WIDGET HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def make_tree(parent, cols, widths=None, height=16):
    wrap = ctk.CTkFrame(parent, fg_color=C["surface"], corner_radius=10, border_width=1, border_color="#555555")
    wrap.pack(fill="both", expand=True, pady=(6, 0))

    tree = ttk.Treeview(wrap, columns=cols, show="headings",
                        height=height, style="T.Treeview")
    for i, c in enumerate(cols):
        w = widths[i] if widths else 140
        tree.heading(c, text=c)
        tree.column(c, width=w, minwidth=50, anchor="w")

    vsb = ttk.Scrollbar(wrap, orient="vertical",   command=tree.yview)
    hsb = ttk.Scrollbar(wrap, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    wrap.grid_rowconfigure(0, weight=1)
    wrap.grid_columnconfigure(0, weight=1)
    
    
    return tree, wrap

def _mpl_defaults(fig, axes):
    fig.patch.set_facecolor(C["chart_bg"])
    for ax in (axes if hasattr(axes, "__iter__") else [axes]):
        ax.set_facecolor(C["chart_bg"])
        ax.tick_params(colors=C["muted"], labelsize=9)
        ax.xaxis.label.set_color(C["muted"])
        ax.yaxis.label.set_color(C["muted"])
        for spine in ax.spines.values():
            spine.set_edgecolor(C["border"])
 
 
def embed_figure(fig, parent):
   
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas
 
def sec_label(parent, text):
    ctk.CTkLabel(parent, text=text,
                 font=("League Spartan", 20, "bold"),
                 text_color=C["text"]).pack(anchor="w", pady=(0, 14))


def mk_btn(parent, text, cmd, color=None, width=130, side="left", padx=4):
    color = color or C["orange"]
    hover = C["mint2"] if color == C["mint"] else C["orange2"]
    b = ctk.CTkButton(parent, text=text, command=cmd,
                      fg_color=color, hover_color=hover,
                      font=("League Spartan", 13, "bold"),
                      corner_radius=8, height=38, width=width,
                      text_color="#0F0F0F" if color == C["mint"] else "#fff")
    b.pack(side=side, padx=padx, pady=0)
    return b


def lbl_entry(parent, label, row, val=""):
    """Label + Entry inside a grid parent. Returns StringVar."""
    ctk.CTkLabel(parent, text=label, font=("League Spartan", 12),
                 text_color=C["muted"]).grid(row=row, column=0,
                 sticky="w", padx=(0, 10), pady=6)
    var = ctk.StringVar(value=val)
    ctk.CTkEntry(parent, textvariable=var, height=36,
                 font=("League Spartan", 12),
                 fg_color=C["surface"], border_color=C["border"],
                 text_color=C["text"]).grid(row=row, column=1,
                 sticky="ew", pady=6)
    return var


def lbl_combo(parent, label, row, values):
    """Label + ComboBox inside a grid parent. Returns StringVar."""
    ctk.CTkLabel(parent, text=label, font=("League Spartan", 12),
                 text_color=C["muted"]).grid(row=row, column=0,
                 sticky="w", padx=(0, 10), pady=6)
    var = ctk.StringVar()
    cb = ctk.CTkComboBox(parent, values=values, variable=var,
                         height=36, font=("League Spartan", 12),
                         fg_color=C["surface"], border_color=C["border"],
                         button_color=C["orange"],
                         dropdown_fg_color=C["card"],
                         text_color=C["text"])
    cb.grid(row=row, column=1, sticky="ew", pady=6)
    if values:
        cb.set(values[0])
        var.set(values[0])
    return var


def search_row(parent, placeholder, on_search):
    """Search bar. Returns entry widget."""
    f = ctk.CTkFrame(parent, fg_color=C["card"], corner_radius=8)
    f.pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(f, text="🔍", font=("League Spartan", 15),
                 text_color=C["muted"]).pack(side="left", padx=(10, 4), pady=8)
    e = ctk.CTkEntry(f, placeholder_text=placeholder, border_width=0,
                     fg_color="transparent", font=("League Spartan", 13),
                     text_color=C["text"],
                     placeholder_text_color=C["muted"])
    e.pack(side="left", fill="x", expand=True, pady=4)
    e.bind("<Return>", lambda _: on_search(e.get()))
    ctk.CTkButton(f, text="Search", command=lambda: on_search(e.get()),
                  fg_color=C["orange"], hover_color=C["orange2"],
                  font=("League Spartan", 13, "bold"),
                  corner_radius=8, height=34, width=100,
                  text_color="#fff").pack(side="right", padx=8, pady=4)
    return e


def metric_card(parent, title, value, color, sub=""):
    f = ctk.CTkFrame(parent, fg_color=C["card"], corner_radius=12,
                     border_width=1, border_color=color)
    f.pack(side="left", padx=8, expand=True, fill="x")
    ctk.CTkLabel(f, text=title, font=("League Spartan", 12),
                 text_color=C["muted"]).pack(pady=(16, 2), padx=12)
    ctk.CTkLabel(f, text=str(value), font=("League Spartan", 26, "bold"),
                 text_color=color).pack()
    ctk.CTkLabel(f, text=sub or " ", font=("League Spartan", 10),
                 text_color=C["muted"]).pack(pady=(2, 14), padx=12)


def tag_status(tree):
    tree.tag_configure("Completed", foreground=C["mint"])
    tree.tag_configure("Cancelled", foreground=C["muted"])
    tree.tag_configure("Pending",   foreground=C["yellow"])


# ═══════════════════════════════════════════════════════════════════════════════
#  DIALOG  (fixed: pure pack layout, no place())
# ═══════════════════════════════════════════════════════════════════════════════
class Dialog(ctk.CTkToplevel):
    """
    Modal dialog with:
      - title bar area (packed top)
      - self.body  : CTkFrame for grid-based form fields (packed, fill both, expand)
      - footer     : added via add_footer()
    """
    def __init__(self, master, title, width=480, height=None):
        super().__init__(master)
        self.title(title)
        self.configure(fg_color=C["card"])
        self.resizable(False, False)
        self.grab_set()
        self.lift()
        self.focus_force()

        if height:
            self.geometry(f"{width}x{height}")
        else:
            self.geometry(f"{width}x380")

        # Center over parent
        self.update_idletasks()
        rx = master.winfo_rootx() + master.winfo_width()  // 2 - self.winfo_width()  // 2
        ry = master.winfo_rooty() + master.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{rx}+{ry}")

        # ── Title bar ────────────────────────────────────────────────────────
        title_bar = ctk.CTkFrame(self, fg_color=C["surface"], corner_radius=0, height=48)
        title_bar.pack(fill="x", side="top")
        title_bar.pack_propagate(False)
        ctk.CTkLabel(title_bar, text=title,
                     font=("League Spartan", 14, "bold"),
                     text_color=C["mint"]).pack(side="left", padx=18, pady=12)

        # ── Body (form area) ─────────────────────────────────────────────────
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True, padx=20, pady=12)
        self.body.columnconfigure(1, weight=1)

    def add_footer(self, ok_text, ok_cmd):
        """Add OK / Cancel footer buttons."""
        footer = ctk.CTkFrame(self, fg_color=C["surface"], corner_radius=0, height=56)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        ctk.CTkButton(footer, text="Cancel", command=self.destroy,
                      fg_color="#3A3A3A", hover_color="#555",
                      font=("League Spartan", 13, "bold"),
                      corner_radius=8, height=36, width=110,
                      text_color="#fff").pack(side="right", padx=(6, 16), pady=10)
        ctk.CTkButton(footer, text=ok_text, command=ok_cmd,
                      fg_color=C["orange"], hover_color=C["orange2"],
                      font=("League Spartan", 13, "bold"),
                      corner_radius=8, height=36, width=150,
                      text_color="#fff").pack(side="right", pady=10)


# ═══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
class DashboardPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._load_data()
 
        # Scrollable container
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent", scrollbar_button_color=C["border"]
        )
        self._scroll.pack(fill="both", expand=True)
 
        sec_label(self._scroll, "📊  Performance Dashboard")
        self._build_cards()
        self._build_charts()
        self._build_pending_table()

    def _load_data(self):
        try:
            self.total_orders = len(ord_db.get_all_orders())
        except:
            self.total_orders = 0

        try:
            self.total_customers = len(cust_db.get_all_customers())
        except:
            self.total_customers = 0

        try:
            rows = rep_db.get_report("vw_deli_success_rate")
            rate = float(rows[0]["success_rate"]) * 100 if rows else 0
            self.delivery_rate = f"{rate:.2f}%"
        except Exception:
            self.delivery_rate = "N/A"
        
        try:

            orders = ord_db.get_all_orders()
            self.total_orders = len(orders)
            total = sum(
                ord_db.get_order_total(o["OrderID"])
                for o in orders
            )
            self.total_revenue = f"{total:,.3f} USD"
        except:

            self.total_orders = 0
            self.total_revenue = "0 USD"
        # ── Chart: Sales per Month ───────────────────────────────────────────
        try:

            rows = rep_db.get_report("vw_sales_per_month")
            rows = sorted(
                rows,
                key=lambda r: (int(r["year"]), int(r["month"]))
            )
            self.month_labels = [
                f"T{int(r['month'])}/{int(r['year'])}"
                for r in rows
            ]
            self.monthly_sales = [
                float(r["revenue"])
                for r in rows
            ]

        except Exception:

            self.month_labels = [
                "T11/2025",
                "T12/2025",
                "T1/2026",
                "T2/2026",
                "T3/2026",
                "T4/2026",
            ]

            self.monthly_sales = [
                4200,
                5100,
                3800,
                6200,
                7400,
                5900
            ]
 
        # ── Chart: Order Status Pie ──────────────────────────────────────────
        try:
            rows = rep_db.get_report("vw_order_status_count")
            self.status_labels = [r["Status"] for r in rows]
            self.status_counts = [int(r["count"]) for r in rows]
        except Exception:
            self.status_labels = ["Completed", "Pending", "Cancelled"]
            self.status_counts = [42, 8, 8]
 
        # ── Table: Pending Orders ────────────────────────────────────────────
        try:
            self.pending_orders = rep_db.get_report("vw_pending_orders")
        except Exception:
            self.pending_orders = []

        # Top Products
        try:
            self.top_products = rep_db.get_report("vw_top_products")
        except:
            self.top_products = [
                {"ProductName": "Vintage Jacket", "total_sold": 152},
                {"ProductName": "Oversized Hoodie", "total_sold": 134},
                {"ProductName": "Cargo Pants", "total_sold": 120},
                {"ProductName": "Basic T-Shirt", "total_sold": 118},
            ]
        # Top Customers
        try:
            self.top_customers = rep_db.get_report("vw_customer_rev")
        except:
            self.top_customers = [
                {"CustomerName": "Alice", "revenue": 12000},
                {"CustomerName": "Bob", "revenue": 9800},
                {"CustomerName": "Charlie", "revenue": 8600},
                {"CustomerName": "David", "revenue": 7200},
            ]
    # ── Metric Cards ─────────────────────────────────────────────────────────
 
    def _build_cards(self):
        
        row = ctk.CTkFrame(self._scroll, fg_color="transparent")
        row.pack(fill="x", pady=(0, 18))
 
        metric_card(row, "💰 Total Revenue",   self.total_revenue,  C["mint"],  "all time")
        metric_card(row, "✅ Delivery Rate",   self.delivery_rate,  C["mint2"], "completed / total")
        metric_card(row, "👥 Total Customers", self.total_customers, C["orange2"],   "registered")
        metric_card(row, "📦 Total Orders",    self.total_orders,   C["orange"], "all statuses")
 
    # ── Charts ───────────────────────────────────────────────────────────────
 
    def _build_charts(self):
 
        # Hàng trên: Line + Bar
        top_row = ctk.CTkFrame(self._scroll, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 12))
        top_row.columnconfigure(0, weight=3)
        top_row.columnconfigure(1, weight=2)
 
        self._chart_monthly(top_row)
        # Hàng dưới: Pie + (chỗ trống dành thêm chart nếu muốn)
        bot_row = ctk.CTkFrame(self._scroll, fg_color="transparent")
        bot_row.pack(fill="x", pady=(0, 12))
        bot_row.columnconfigure(0, weight=1)
        bot_row.columnconfigure(1, weight=2)
 
        self._chart_pie(top_row)
        self._chart_top_products(bot_row)
        self._chart_top_customers(bot_row)
    # ── Line chart: Sales per Month ──────────────────────────────────────────
 
    def _chart_monthly(self, parent):
        card = ctk.CTkFrame(parent, fg_color=C["card"], corner_radius=12 )
        card.grid( row=0, column=0, sticky="nsew", padx=(0, 6))
        ctk.CTkLabel( card, text="📈  Sales per Month", font=("League Spartan", 13, "bold"), text_color=C["muted"]
        ).pack(
            anchor="w",
            padx=14,
            pady=(12, 0)
        )

        fig = Figure(figsize=(5.0, 2.8), dpi=96)
        ax = fig.add_subplot(111)
        _mpl_defaults(fig, ax)
        x = range(len(self.monthly_sales))
        ax.plot( x, self.monthly_sales, color=C["mint"], linewidth=2.2, marker="o", markersize=4, markerfacecolor=C["green"])
        ax.fill_between( x, self.monthly_sales, alpha=0.12, color=C["mint2"])
        ax.set_xticks(list(x))

        ax.set_xticklabels( self.month_labels, fontsize=8, rotation=30)

        ax.yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(
                lambda v, _:
                    f"${v/1000:.0f}k"
                    if v >= 1000
                    else f"${v:.0f}"
            )
        )

        ax.grid(axis="y", color=C["border"], linestyle="--", linewidth=0.6)
        fig.tight_layout(pad=1.2)
        embed_figure(fig, card)
        
    # --- Bar chart Top Products ----------------------------------------------
    def _chart_top_products(self, parent):
        card = ctk.CTkFrame(parent, fg_color=C["card"], corner_radius=12)
        card.grid(row=1, column=0, sticky="nsew")

        ctk.CTkLabel(
            card, text="🏆 Top Products",
            font=("League Spartan", 13, "bold"),
            text_color=C["muted"]
        ).pack(anchor="w", padx=14, pady=(12, 0))

        fig = Figure(figsize=(4.5, 2.8), dpi=96)
        ax = fig.add_subplot(111)

        _mpl_defaults(fig, ax)

        names = [r["ProductName"] for r in self.top_products]
        sales = [int(r["total_sold"]) for r in self.top_products]

        ax.barh(names, sales, color=C["orange2"], alpha=0.9)
        ax.invert_yaxis()
        ax.grid(
            axis="x",
            color=C["border"],
            linestyle="--",
            linewidth=0.6
        )

        fig.tight_layout(pad=1.2)

        embed_figure(fig, card)
 
    # ── Pie chart: Order Status ──────────────────────────────────────────────
 
    def _chart_pie(self, parent):
        card = ctk.CTkFrame(parent, fg_color=C["card"], corner_radius=12)
        card.grid(row=0, column=1, sticky="nsew", padx=(0, 6))
 
        ctk.CTkLabel(
            card, text="🥧 Orders Status",
            font=("League Spartan", 13, "bold"),
            text_color=C["muted"]
        ).pack(anchor="w", padx=14, pady=(12, 0))
 
        palette = [C["red"], C["mint"], C["orange"]]
        pie_colors = palette[:len(self.status_labels)]
 
        fig = Figure(figsize=(3.0, 2.8), dpi=96)
        ax  = fig.add_subplot(111)
        _mpl_defaults(fig, ax)
 
        wedges, texts, autotexts = ax.pie(
            self.status_counts,
            labels=None,
            colors=pie_colors,
            autopct="%1.0f%%",
            startangle=140,
            wedgeprops={"linewidth": 0.8, "edgecolor": C["chart_bg"]},
            pctdistance=0.75
        )
        for at in autotexts:
            at.set_fontsize(9)
            at.set_color(C["bg"])
            at.set_fontweight("bold")
 
        # Legend ngoài
        patches = [mpatches.Patch(color=c, label=l)
                   for c, l in zip(pie_colors, self.status_labels)]
        ax.legend(handles=patches, loc="center left",
                  bbox_to_anchor=(1.0, 0.5),
                  fontsize=9, frameon=False,
                  labelcolor=C["text"])
 
        fig.tight_layout(pad=1.0)
        embed_figure(fig, card)
    # --- Top Customers -------------------------------------------------------
    def _chart_top_customers(self, parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=C["card"],
            corner_radius=12,
            width=420,
            height=260
        )

        card.grid(row=1, column=1, sticky="nsew", padx=(6, 0))
        card.grid_propagate(False)

        ctk.CTkLabel(
            card,
            text="👑 Top Customers",
            font=("League Spartan", 13, "bold"),
            text_color=C["muted"]
        ).pack(anchor="w", padx=14, pady=(12, 0))

        fig = Figure(figsize=(4.2, 2.8), dpi=96)

        ax = fig.add_subplot(111)

        _mpl_defaults(fig, ax)

        names = [r["CustomerName"] for r in self.top_customers]
        revenue = [float(r["revenue"]) for r in self.top_customers]

        ax.bar(names, revenue, color=C["mint"], alpha=0.9)

        ax.set_xticklabels(
            names,
            rotation=20,
            fontsize=8
        )

        ax.yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(
                lambda v, _:
                    f"${v/1000:.0f}k"
                    if v >= 1000
                    else f"${v:.0f}"
            )
        )

        ax.grid(
            axis="y",
            color=C["border"],
            linestyle="--",
            linewidth=0.6
        )

        fig.tight_layout(pad=1.2)

        embed_figure(fig, card)
    # ── Pending Orders Table ─────────────────────────────────────────────────
 
    def _build_pending_table(self):
        ctk.CTkLabel(
            self._scroll,
            text="⏳ Pending Orders Lists",
            font=("League Spartan", 14, "bold"),
            text_color=C["muted"]
        ).pack(anchor="w", pady=(8, 0))
 
        cols   = ["OrderID", "CustomerName", "PhoneNumber", "OrderDate", "Status"]
        widths = [80, 200, 160, 130, 100]
        tree, _ = make_tree(self._scroll, cols, widths, height=10)
 
        tree.tag_configure("Pending",    foreground=C["yellow"])
        tree.tag_configure("Processing", foreground=C["blue"])
        tree.tag_configure("Cancelled",  foreground=C["red"])
 
        for r in self.pending_orders:
            status = r.get("Status", "Pending")
            tree.insert(
                "", "end",
                values=(r.get("OrderID"), r.get("CustomerName"),
                        r.get("PhoneNumber"), r.get("OrderDate"), status),
                tags=(status,)
            )
 
    # -- Top Products --------------------------------------------------------
    
# ═══════════════════════════════════════════════════════════════════════════════
#  CUSTOMERS
# ═══════════════════════════════════════════════════════════════════════════════
class CustomersPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._sel = None
        sec_label(self, "👤  Customer Management")
        search_row(self, "Search by Name or Phone…", self._search)

        tb = ctk.CTkFrame(self, fg_color="transparent")
        tb.pack(fill="x", pady=(0, 6))
        mk_btn(tb, "＋ Add",       self._dlg_add,     C["mint"],   140)
        mk_btn(tb, "✏ Edit",       self._dlg_edit,    C["orange"], 110)
        mk_btn(tb, "🗑 Delete",    self._delete,      "#444",      110)
        mk_btn(tb, "📋 History",   self._history,     "#444",      130)
        mk_btn(tb, "↻ Refresh",    self._load,        "#333",      110, "right", 0)

        cols   = ["ID", "Name", "Address", "Phone"]
        widths = [70, 230, 310, 170]
        self._tree, _ = make_tree(self, cols, widths, height=19)
        self._tree.bind("<<TreeviewSelect>>", self._on_sel)
        self._load()

    # ── data ─────────────────────────────────────────────────────────────────
    def _load(self, data=None):
        data = data or cust_db.get_all_customers()
        self._tree.delete(*self._tree.get_children())
        for r in sorted(data, key=lambda x: x["CustomerID"]):
            self._tree.insert("", "end", iid=r["CustomerID"],
                values=(r["CustomerID"], r["CustomerName"],
                        r["Address"] or "", r["PhoneNumber"] or ""))

    def _search(self, q):
        self._load(cust_db.search_customer(q) if q.strip() else None)

    def _on_sel(self, _):
        s = self._tree.selection()
        self._sel = int(s[0]) if s else None

    def _require_sel(self):
        if not self._sel:
            messagebox.showwarning("No Selection", "Select a customer first.")
            return False
        return True

    # ── dialogs ──────────────────────────────────────────────────────────────
    def _dlg_add(self):
        d = Dialog(self.winfo_toplevel(), "Add New Customer", 480, 290)
        n = lbl_entry(d.body, "Full Name", 0)
        a = lbl_entry(d.body, "Address",   1)
        p = lbl_entry(d.body, "Phone",     2)
        def _ok():
            if not n.get().strip():
                messagebox.showerror("Validation", "Name is required.", parent=d); return
            try:
                cust_db.add_customer(n.get().strip(), a.get().strip(), p.get().strip())
                d.destroy(); self._load()
                messagebox.showinfo("Success", "Customer added.")
            except Exception as e:
                messagebox.showerror("DB Error", str(e), parent=d)
        d.add_footer("Add Customer", _ok)

    def _dlg_edit(self):
        if not self._require_sel(): return
        rec = cust_db.get_customer_by_id(self._sel)
        if not rec: return
        d = Dialog(self.winfo_toplevel(), "Edit Customer", 480, 290)
        n = lbl_entry(d.body, "Full Name", 0, rec["CustomerName"])
        a = lbl_entry(d.body, "Address",   1, rec["Address"] or "")
        p = lbl_entry(d.body, "Phone",     2, rec["PhoneNumber"] or "")
        def _ok():
            try:
                cust_db.update_customer(self._sel, n.get().strip(),
                                        a.get().strip(), p.get().strip())
                d.destroy(); self._load()
                messagebox.showinfo("Success", "Customer updated.")
            except Exception as e:
                messagebox.showerror("DB Error", str(e), parent=d)
        d.add_footer("Save Changes", _ok)

    def _delete(self):
        if not self._require_sel(): return
        if messagebox.askyesno("Confirm", f"Delete Customer #{self._sel}?"):
            try:
                cust_db.delete_customer(self._sel)
                self._sel = None; self._load()
            except Exception as e:
                messagebox.showerror("DB Error", str(e))

    def _history(self):
        if not self._require_sel(): return
        rec     = cust_db.get_customer_by_id(self._sel)
        history = cust_db.get_customer_order_history(self._sel)

        d = Dialog(self.winfo_toplevel(), f"Order History — {rec['CustomerName']}", 640, 460)
        d.body.rowconfigure(0, weight=1)
        d.body.columnconfigure(0, weight=1)
        d.body.columnconfigure(1, weight=1)

        # tree fills body
        wrap = ctk.CTkFrame(d.body, fg_color=C["purple"], corner_radius=10)
        wrap.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 8))
        wrap.grid_rowconfigure(0, weight=1)
        wrap.grid_columnconfigure(0, weight=1)

        cols   = ["OrderID", "Date", "Status", "Total"]
        widths = [90, 130, 120, 160]
        tree   = ttk.Treeview(wrap, columns=cols, show="headings",
                               height=10, style="T.Treeview")
        for c, w in zip(cols, widths):
            tree.heading(c, text=c); tree.column(c, width=w, anchor="w")
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        tag_status(tree)
        total_spend = 0.0
        for r in history:
            amt = float(r["TotalAmount"]) if r["TotalAmount"] else 0.0
            total_spend += amt
            tree.insert("", "end",
                values=(r["OrderID"], r["OrderDate"], r["Status"], f"{amt:,.2f}"),
                tags=(r["Status"],))

        ctk.CTkLabel(d.body,
                     text=f"Lifetime Spending:  {total_spend:,.2f}",
                     font=("League Spartan", 13, "bold"),
                     text_color=C["mint"]).grid(row=1, column=0, sticky="w", pady=4)
        ctk.CTkButton(d.body, text="Close", command=d.destroy,
                      fg_color=C["orange"], hover_color=C["orange2"],
                      font=("League Spartan", 13, "bold"),
                      corner_radius=8, height=34, width=100,
                      text_color="#fff").grid(row=1, column=1, sticky="e", pady=4)


# ═══════════════════════════════════════════════════════════════════════════════
#  PRODUCTS
# ═══════════════════════════════════════════════════════════════════════════════
class ProductsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._sel = None
        sec_label(self, "📦  Product Management")
        search_row(self, "Search by Name or Product ID…", self._search)

        tb = ctk.CTkFrame(self, fg_color="transparent")
        tb.pack(fill="x", pady=(0, 6))
        mk_btn(tb, "＋ Add",      self._dlg_add,     C["mint"],   130)
        mk_btn(tb, "✏ Edit",      self._dlg_edit,    C["orange"], 110)
        mk_btn(tb, "🗑 Delete",   self._delete,      C["red"],      110)
        mk_btn(tb, "🔄 Restock",  self._dlg_restock, C["purple"],      120)
        mk_btn(tb, "📈 Sold Quanity",    self._sales_count, C["blue"],      110)
        mk_btn(tb, "⚠ Low Stock", self._show_low,    C["red"],    120)
        mk_btn(tb, "↻ Refresh",   self._load,        "#333",      110, "right", 0)

        cols   = ["ID", "Product Name", "Price", "Stock"]
        widths = [70, 300, 130, 110]
        self._tree, _ = make_tree(self, cols, widths, height=19)
        self._tree.tag_configure("low", foreground=C["red"])
        self._tree.bind("<<TreeviewSelect>>", self._on_sel)
        self._load()

    def _load(self, data=None):
        data = data or prod_db.get_all_products()
        self._tree.delete(*self._tree.get_children())
        for r in sorted(data, key=lambda x: x["ProductID"]):
            tag = "low" if r["StockQuantity"] < 10 else ""
            self._tree.insert("", "end", iid=r["ProductID"],
                values=(r["ProductID"], r["ProductName"],
                        f"{float(r['Price']):,.2f}", r["StockQuantity"]),
                tags=(tag,))

    def _search(self, q):
        if not q.strip(): self._load(); return
        if q.strip().isdigit():
            r = prod_db.get_product_by_id(int(q.strip()))
            self._load([r] if r else [])
        else:
            self._load(prod_db.search_product_by_name(q.strip()))

    def _on_sel(self, _):
        s = self._tree.selection()
        self._sel = int(s[0]) if s else None

    def _require_sel(self):
        if not self._sel:
            messagebox.showwarning("No Selection", "Select a product first.")
            return False
        return True

    def _dlg_add(self):
        d = Dialog(self.winfo_toplevel(), "Add New Product", 480, 300)
        n = lbl_entry(d.body, "Product Name", 0)
        p = lbl_entry(d.body, "Price",        1, "0.00")
        s = lbl_entry(d.body, "Stock Qty",    2, "0")
        def _ok():
            try:
                prod_db.add_product(n.get().strip(), float(p.get()), int(s.get()))
                d.destroy(); self._load()
                messagebox.showinfo("Success", "Product added.")
            except Exception as e:
                messagebox.showerror("DB Error", str(e), parent=d)
        d.add_footer("Add Product", _ok)

    def _dlg_edit(self):
        if not self._require_sel(): return
        rec = prod_db.get_product_by_id(self._sel)
        if not rec: return
        d = Dialog(self.winfo_toplevel(), "Edit Product", 480, 300)
        n = lbl_entry(d.body, "Product Name", 0, rec["ProductName"])
        p = lbl_entry(d.body, "Price",        1, str(rec["Price"]))
        s = lbl_entry(d.body, "Stock Qty",    2, str(rec["StockQuantity"]))
        def _ok():
            try:
                prod_db.update_product(self._sel, n.get().strip(),
                                       float(p.get()), int(s.get()))
                d.destroy(); self._load()
                messagebox.showinfo("Success", "Product updated.")
            except Exception as e:
                messagebox.showerror("DB Error", str(e), parent=d)
        d.add_footer("Save Changes", _ok)

    def _delete(self):
        if not self._require_sel(): return
        if messagebox.askyesno("Confirm", f"Delete Product #{self._sel}?"):
            try:
                prod_db.delete_product(self._sel)
                self._sel = None; self._load()
            except Exception as e:
                messagebox.showerror("DB Error", str(e))

    def _dlg_restock(self):
        if not self._require_sel(): return
        rec = prod_db.get_product_by_id(self._sel)
        if not rec: return
        d = Dialog(self.winfo_toplevel(), f"Restock — {rec['ProductName']}", 480, 250)
        ctk.CTkLabel(d.body, text=f"Current stock: {rec['StockQuantity']} units",
                     font=("League Spartan", 12), text_color=C["muted"]
                     ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        qty = lbl_entry(d.body, "Add Quantity", 1, "0")
        def _ok():
            try:
                q = int(qty.get())
                if q <= 0:
                    messagebox.showerror("Validation", "Qty must be > 0.", parent=d); return
                inv_db.restock(self._sel, q)
                d.destroy(); self._load()
                messagebox.showinfo("Restocked", f"Added {q} units.")
            except Exception as e:
                messagebox.showerror("DB Error", str(e), parent=d)
        d.add_footer("Restock", _ok)

    def _sales_count(self):
        if not self._require_sel(): return
        rec   = prod_db.get_product_by_id(self._sel)
        count = prod_db.get_product_sales_count(self._sel)
        messagebox.showinfo("Sales Performance",
                            f"Product:  {rec['ProductName']}\n"
                            f"Units Sold:  {count}")

    def _show_low(self):
        data = inv_db.get_low_stock(10)
        d = Dialog(self.winfo_toplevel(), "⚠  Low Stock Alert", 460, 420)
        d.body.rowconfigure(0, weight=1)
        d.body.columnconfigure(0, weight=1)
        d.body.columnconfigure(1, weight=1)

        wrap = ctk.CTkFrame(d.body, fg_color=C["surface"], corner_radius=10)
        wrap.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 8))
        wrap.grid_rowconfigure(0, weight=1); wrap.grid_columnconfigure(0, weight=1)

        cols   = ["ProductID", "Product Name", "Stock"]
        widths = [80, 230, 80]
        tree   = ttk.Treeview(wrap, columns=cols, show="headings",
                               height=10, style="T.Treeview")
        for c, w in zip(cols, widths):
            tree.heading(c, text=c); tree.column(c, width=w, anchor="w")
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        tree.tag_configure("danger", foreground=C["red"])
        for r in data:
            tree.insert("", "end",
                values=(r["ProductID"], r["ProductName"], r["StockQuantity"]),
                tags=("danger",))

        ctk.CTkLabel(d.body, text=f"{len(data)} product(s) below threshold",
                     font=("League Spartan", 11), text_color=C["muted"]
                     ).grid(row=1, column=0, sticky="w", pady=6)
        ctk.CTkButton(d.body, text="Close", command=d.destroy,
                      fg_color=C["orange"], hover_color=C["orange2"],
                      font=("League Spartan", 13, "bold"),
                      corner_radius=8, height=34, width=100,
                      text_color="#fff").grid(row=1, column=1, sticky="e", pady=6)


# ═══════════════════════════════════════════════════════════════════════════════
#  ORDERS
# ═══════════════════════════════════════════════════════════════════════════════
class OrdersPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._sel = None
        sec_label(self, "🛒  Order Management")

        tb = ctk.CTkFrame(self, fg_color="transparent")
        tb.pack(fill="x", pady=(0, 6))
        mk_btn(tb, "＋ New Order",  self._dlg_new,   C["mint"],   150)
        mk_btn(tb, "📋 View Items", self._view_items, C["orange"], 130)
        mk_btn(tb, "✔ Complete",    self._complete,   C["green"],  120)
        mk_btn(tb, "✖ Cancel",      self._cancel,     C["red"],    110)
        mk_btn(tb, "↻ Refresh",     self._load,       "#333",      110, "right", 0)

        cols   = ["OrderID", "Customer", "Employee", "Date", "Status"]
        widths = [80, 210, 190, 120, 110]
        self._tree, _ = make_tree(self, cols, widths, height=20)
        tag_status(self._tree)
        self._tree.bind("<<TreeviewSelect>>", self._on_sel)
        self._load()

    def _load(self):
        orders = ord_db.get_all_orders()
        self._tree.delete(*self._tree.get_children())
        for o in orders:
            self._tree.insert("", "end", iid=o["OrderID"],
                values=(o["OrderID"], o["CustomerName"],
                        o["EmployeeName"], o["OrderDate"], o["Status"]),
                tags=(o["Status"],))

    def _on_sel(self, _):
        s = self._tree.selection()
        self._sel = int(s[0]) if s else None

    def _require_sel(self):
        if not self._sel:
            messagebox.showwarning("No Selection", "Select an order first.")
            return False
        return True

    # ── view items ────────────────────────────────────────────────────────────
    def _view_items(self):
        if not self._require_sel(): return
        items = ord_db.get_order_items(self._sel)
        total = ord_db.get_order_total(self._sel)
        final = ord_db.get_order_final_price(self._sel)
        disc  = total - final

        d = Dialog(self.winfo_toplevel(), f"Order #{self._sel} — Items", 680, 500)
        d.body.rowconfigure(0, weight=1)
        d.body.columnconfigure(0, weight=1)
        d.body.columnconfigure(1, weight=1)

        wrap = ctk.CTkFrame(d.body, fg_color=C["surface"], corner_radius=10)
        wrap.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 8))
        wrap.grid_rowconfigure(0, weight=1); wrap.grid_columnconfigure(0, weight=1)

        cols   = ["ProductID", "Product Name", "Quantity", "Sales Price", "Subtotal"]
        widths = [80, 220, 60, 120, 130]
        tree   = ttk.Treeview(wrap, columns=cols, show="headings",
                               height=10, style="T.Treeview")
        for c, w in zip(cols, widths):
            tree.heading(c, text=c); tree.column(c, width=w, anchor="w")
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        for r in items:
            tree.insert("", "end",
                values=(r["ProductID"], r["ProductName"], r["Quantity"],
                        f"{float(r['SalePrice']):,.2f}",
                        f"{float(r['SubTotal']):,.2f}"))

        summary = (f"Subtotal: {total:,.2f}   |   "
                   f"Discount: -{disc:,.2f}   |   "
                   f"Final: {final:,.2f}")
        ctk.CTkLabel(d.body, text=summary,
                     font=("League Spartan", 12, "bold"),
                     text_color=C["mint"]).grid(row=1, column=0, sticky="w", pady=6)
        ctk.CTkButton(d.body, text="Close", command=d.destroy,
                      fg_color=C["orange"], hover_color=C["orange2"],
                      font=("League Spartan", 13, "bold"),
                      corner_radius=8, height=34, width=100,
                      text_color="#fff").grid(row=1, column=1, sticky="e", pady=6)

    # ── complete / cancel ─────────────────────────────────────────────────────
    def _complete(self):
        if not self._require_sel(): return
        if messagebox.askyesno("Confirm", f"Mark Order #{self._sel} as Completed?"):
            try:
                ord_db.complete_order(self._sel); self._load()
                messagebox.showinfo("Done", f"Order #{self._sel} completed.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _cancel(self):
        if not self._require_sel(): return
        if messagebox.askyesno("Confirm Cancel",
                f"Cancel Order #{self._sel}?\nStock restored automatically by DB trigger."):
            try:
                ord_db.cancel_order(self._sel); self._load()
                messagebox.showinfo("Cancelled",
                    f"Order #{self._sel} cancelled.\nStock restored via trigger.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # ── new order ─────────────────────────────────────────────────────────────
    def _dlg_new(self):
        d = Dialog(self.winfo_toplevel(), "Create New Order", 740, 600)
        d.body.columnconfigure(1, weight=1)

        # Customer
        customers = cust_db.get_all_customers()
        c_map = {f"{c['CustomerID']} — {c['CustomerName']}": c["CustomerID"]
                 for c in customers}
        c_var = lbl_combo(d.body, "Customer", 0, list(c_map.keys()))

        # Employee
        employees = emp_db.get_all_employees()
        e_map = {f"{e['EmployeeID']} — {e['EmployeeName']} ({e['JobTitle']})": e["EmployeeID"]
                 for e in employees}
        e_var = lbl_combo(d.body, "Employee", 1, list(e_map.keys()))

        # Items header
        ctk.CTkLabel(d.body, text="Order Items",
                     font=("League Spartan", 12, "bold"),
                     text_color=C["mint"]).grid(
                     row=2, column=0, columnspan=2, sticky="w", pady=(12, 4))

        # Column labels
        hf = ctk.CTkFrame(d.body, fg_color="transparent")
        hf.grid(row=3, column=0, columnspan=2, sticky="ew")
        ctk.CTkLabel(hf, text="Product",
                     font=("League Spartan", 11), text_color=C["muted"],
                     anchor="w").pack(side="left", padx=(2, 8), fill="x", expand=True)
        ctk.CTkLabel(hf, text="Qty",
                     font=("League Spartan", 11), text_color=C["muted"],
                     width=70, anchor="w").pack(side="left")

        # Scrollable item rows
        sf = ctk.CTkScrollableFrame(d.body, fg_color=C["surface"],
                                    corner_radius=8, height=200)
        sf.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 6))
        sf.columnconfigure(0, weight=1)

        products = prod_db.get_all_products()
        p_keys = [f"{p['ProductID']} — {p['ProductName']}  [stock:{p['StockQuantity']}]"
                  for p in products]
        p_map  = {f"{p['ProductID']} — {p['ProductName']}  [stock:{p['StockQuantity']}]":
                  p["ProductID"] for p in products}

        item_rows = []   # list of (p_StringVar, q_StringVar)

        def add_row():
            rf = ctk.CTkFrame(sf, fg_color="transparent")
            rf.grid(row=len(item_rows), column=0, sticky="ew", pady=3)
            rf.columnconfigure(0, weight=1)
            pv = ctk.StringVar(value=p_keys[0] if p_keys else "")
            qv = ctk.StringVar(value="1")
            ctk.CTkComboBox(rf, values=p_keys, variable=pv,
                            font=("League Spartan", 11),
                            fg_color=C["card"], border_color=C["border"],
                            button_color=C["orange"],
                            dropdown_fg_color=C["card"],
                            text_color=C["text"], width=530
                            ).grid(row=0, column=0, sticky="ew", padx=(4, 8))
            ctk.CTkEntry(rf, textvariable=qv, width=70,
                         font=("League Spartan", 11),
                         fg_color=C["card"], border_color=C["border"],
                         text_color=C["text"]
                         ).grid(row=0, column=1, padx=(0, 4))
            item_rows.append((pv, qv))

        add_row()   # first row by default

        ctk.CTkButton(d.body, text="＋ Add Line", command=add_row,
                      fg_color="#333", hover_color="#555",
                      font=("League Spartan", 12, "bold"),
                      corner_radius=8, height=32, width=130,
                      text_color="#fff").grid(
                      row=5, column=0, sticky="w", pady=(2, 0))

        def _ok():
            try:
                cid = c_map.get(c_var.get())
                eid = e_map.get(e_var.get())
                if not cid or not eid:
                    messagebox.showerror("Validation",
                        "Select both Customer and Employee.", parent=d); return
                items = []
                for pv, qv in item_rows:
                    pid = p_map.get(pv.get())
                    try: qty = int(qv.get())
                    except ValueError: qty = 0
                    if pid and qty > 0:
                        items.append((pid, qty))
                if not items:
                    messagebox.showerror("Validation",
                        "Add at least one valid item.", parent=d); return
                oid = ord_db.create_order(cid, eid, items)
                d.destroy(); self._load()
                messagebox.showinfo("Created", f"Order #{oid} created successfully!")
            except Exception as e:
                messagebox.showerror("DB Error", str(e), parent=d)

        d.add_footer("Create Order", _ok)


# ═══════════════════════════════════════════════════════════════════════════════
#  EMPLOYEES
# ═══════════════════════════════════════════════════════════════════════════════
class EmployeesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._sel = None
        sec_label(self, "👥  Employee Management")

        tb = ctk.CTkFrame(self, fg_color="transparent")
        tb.pack(fill="x", pady=(0, 6))
        mk_btn(tb, "📋 View Assigned Orders", self._show_orders, C["orange"], 200)
        mk_btn(tb, "↻ Refresh",               self._load,        "#333",      110, "right", 0)

        cols   = ["ID", "Employee Name", "Job Title"]
        widths = [70, 280, 220]
        self._tree, _ = make_tree(self, cols, widths, height=22)
        self._tree.bind("<<TreeviewSelect>>", self._on_sel)
        self._load()

    def _load(self):
        data = emp_db.get_all_employees()
        self._tree.delete(*self._tree.get_children())
        for r in data:
            self._tree.insert("", "end", iid=r["EmployeeID"],
                values=(r["EmployeeID"], r["EmployeeName"], r["JobTitle"]))

    def _on_sel(self, _):
        s = self._tree.selection()
        self._sel = int(s[0]) if s else None

    def _show_orders(self):
        if not self._sel:
            messagebox.showwarning("No Selection", "Select an employee first."); return

        emp    = emp_db.get_employee_by_id(self._sel)
        orders = emp_db.get_orders_by_employee(self._sel)

        d = Dialog(self.winfo_toplevel(),
                   f"Orders by {emp['EmployeeName']}", 620, 460)
        d.body.rowconfigure(0, weight=1)
        d.body.columnconfigure(0, weight=1)
        d.body.columnconfigure(1, weight=1)

        wrap = ctk.CTkFrame(d.body, fg_color=C["surface"], corner_radius=10)
        wrap.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 8))
        wrap.grid_rowconfigure(0, weight=1); wrap.grid_columnconfigure(0, weight=1)

        cols   = ["OrderID", "Date", "Status", "Customer"]
        widths = [80, 130, 110, 230]
        tree   = ttk.Treeview(wrap, columns=cols, show="headings",
                               height=11, style="T.Treeview")
        for c, w in zip(cols, widths):
            tree.heading(c, text=c); tree.column(c, width=w, anchor="w")
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        tag_status(tree)
        for o in orders:
            tree.insert("", "end",
                values=(o["OrderID"], o["OrderDate"], o["Status"], o["CustomerName"]),
                tags=(o["Status"],))

        ctk.CTkLabel(d.body, text=f"Total handled: {len(orders)} orders",
                     font=("League Spartan", 12), text_color=C["muted"]
                     ).grid(row=1, column=0, sticky="w", pady=6)
        ctk.CTkButton(d.body, text="Close", command=d.destroy,
                      fg_color=C["orange"], hover_color=C["orange2"],
                      font=("League Spartan", 13, "bold"),
                      corner_radius=8, height=34, width=100,
                      text_color="#fff").grid(row=1, column=1, sticky="e", pady=6)


# ═══════════════════════════════════════════════════════════════════════════════
#  REPORTS
# ═══════════════════════════════════════════════════════════════════════════════
class ReportsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        sec_label(self, "📈  Reports & Analytics")

        tabs = ctk.CTkTabview(
            self,
            fg_color=C["card"],
            corner_radius=10,
            segmented_button_fg_color=C["surface"],
            segmented_button_selected_color=C["orange"],
            segmented_button_unselected_color=C["surface"],
            segmented_button_selected_hover_color=C["orange2"],
            text_color=C["text"],
        )
        tabs.pack(fill="both", expand=True)

        report_tabs = [
            ("🏆 Top Products",     "vw_top_products",
             ["ProductName", "total_sold", "ranking"]),
            ("📅 Monthly Sales",    "vw_sales_per_month",
             ["year", "month", "revenue"]),
            ("👤 Customer Revenue", "vw_customer_rev",
             ["customername", "revenue"]),
            ("📦 Inventory Value",  "vw_inventory_value",
             ["ProductName", "StockQuantity", "Price", "total_value"]),
            ("🚚 Delivery Rate",    "vw_deli_success_rate",
             ["success_rate"]),
            ("📋 Daily Orders",     "vw_daily_orders",
             ["OrderDate", "total_orders"]),
            ("💰 Daily Sales",      "vw_daily_sales",
             ["OrderDate", "Revenue"]),
            ("⚠ Low Stock",         "vw_low_stock",
             ["ProductName", "StockQuantity"]),
            ("📊 Sales/Product",    "vw_sales_per_product",
             ["ProductID", "ProductName", "Total_sold", "Revenue"]),
        ]

        for tab_name, view, cols in report_tabs:
            tab = tabs.add(tab_name)
            tab.configure(fg_color="transparent")
            self._build_tab(tab, view, cols)

    def _build_tab(self, parent, view_name, cols):
        def load():
            try:
                data = rep_db.get_report(view_name)
                tree.delete(*tree.get_children())
                for r in data:
                    tree.insert("", "end", values=[r.get(c, "") for c in cols])
            except Exception as e:
                messagebox.showerror("Report Error", str(e))

        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="both", expand=True)
        ctk.CTkButton(f, text="↻ Refresh", command=load,
                      fg_color="#333", hover_color="#555",
                      font=("League Spartan", 12, "bold"),
                      corner_radius=8, height=32, width=110,
                      text_color="#fff").pack(anchor="e", pady=(6, 4))
        tree, _ = make_tree(f, cols, height=15)
        load()


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN WINDOW
# ═══════════════════════════════════════════════════════════════════════════════
class SalesApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        apply_tree_style()
        self.title("Sales Pro — Management System")
        self.geometry("1440x900")
        self.minsize(1100, 700)
        self.configure(fg_color=C["bg"])
        self._active_btn = None
        self._build()
        self._show("Dashboard")

    def _build(self):
        # ── Sidebar ───────────────────────────────────────────────────────────
        sb = ctk.CTkFrame(self, width=228, corner_radius=0, fg_color=C["sidebar"])
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        logo = ctk.CTkFrame(sb, fg_color="transparent")
        logo.pack(pady=(36, 4), padx=22, anchor="w")
        ctk.CTkLabel(logo, text="SALES", font=("League Spartan", 28, "bold"),
                     text_color=C["mint"]).pack(side="left")
        ctk.CTkLabel(logo, text=" PRO", font=("League Spartan", 28, "bold"),
                     text_color=C["orange"]).pack(side="left")
        ctk.CTkLabel(sb, text="Management System",
                     font=("League Spartan", 11),
                     text_color=C["muted"]).pack(anchor="w", padx=24, pady=(0, 18))
        ctk.CTkFrame(sb, height=1, fg_color=C["border"]).pack(fill="x", padx=20, pady=(0, 14))

        nav = [("📊", "Dashboard"), ("👤", "Customers"), ("📦", "Products"),
               ("🛒", "Orders"),    ("👥", "Employees"), ("📈", "Reports")]
        self._nav_btns = {}
        for icon, key in nav:
            b = ctk.CTkButton(sb, text=f"  {icon}  {key}",
                              font=("League Spartan", 14),
                              fg_color="transparent", text_color=C["text"],
                              hover_color=C["surface"], anchor="w",
                              height=48, corner_radius=8,
                              command=lambda k=key: self._show(k))
            b.pack(fill="x", padx=12, pady=2)
            self._nav_btns[key] = b

        ctk.CTkFrame(sb, height=1, fg_color=C["border"]).pack(
            fill="x", padx=20, side="bottom", pady=14)
        ctk.CTkLabel(sb, text="v1.0  •  Dark Mode",
                     font=("League Spartan", 10),
                     text_color=C["muted"]).pack(side="bottom", pady=(0, 6))

        # ── Content ───────────────────────────────────────────────────────────
        self._content = ctk.CTkFrame(self, fg_color="transparent")
        self._content.pack(side="right", fill="both", expand=True, padx=32, pady=26)

    def _show(self, key):
        if self._active_btn:
            self._active_btn.configure(fg_color="transparent", text_color=C["text"])
        self._active_btn = self._nav_btns[key]
        self._active_btn.configure(fg_color=C["surface"], text_color=C["mint"])

        for w in self._content.winfo_children():
            w.destroy()

        pages = {
            "Dashboard" : DashboardPage,
            "Customers" : CustomersPage,
            "Products"  : ProductsPage,
            "Orders"    : OrdersPage,
            "Employees" : EmployeesPage,
            "Reports"   : ReportsPage,
        }
        pages[key](self._content).pack(fill="both", expand=True)


if __name__ == "__main__":
    app = SalesApp()
    app.mainloop()