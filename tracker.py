import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

FILE_NAME = "expenses.csv"

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("900x650")
        self.root.configure(bg="#f0f0f0")
        
        # Color scheme
        self.colors = {
            "primary": "#2563eb",
            "secondary": "#64748b",
            "success": "#10b981",
            "danger": "#ef4444",
            "light": "#f8fafc",
            "dark": "#1e293b",
            "border": "#e2e8f0"
        }

        self.create_file()
        self.setup_styles()
        self.create_widgets()
        self.load_expenses()

    def create_file(self):
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Amount"])

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure Treeview
        style.configure("Treeview",
                       background=self.colors["light"],
                       foreground=self.colors["dark"],
                       rowheight=30,
                       fieldbackground=self.colors["light"],
                       borderwidth=0)
        style.map('Treeview', background=[('selected', self.colors["primary"])])
        
        style.configure("Treeview.Heading",
                       background=self.colors["secondary"],
                       foreground="white",
                       relief="flat",
                       font=('Segoe UI', 10, 'bold'))
        style.map("Treeview.Heading",
                 background=[('active', self.colors["primary"])])

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors["primary"], height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="💰 Expense Tracker",
                              font=('Segoe UI', 24, 'bold'),
                              bg=self.colors["primary"],
                              fg="white")
        title_label.pack(pady=20)

        # Main container
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Input section
        input_frame = tk.Frame(main_container, bg="white", relief="flat", bd=0)
        input_frame.pack(fill="x", pady=(0, 20))
        
        # Add subtle shadow effect with border
        input_frame.configure(highlightbackground=self.colors["border"], 
                            highlightthickness=1)
        
        inner_frame = tk.Frame(input_frame, bg="white")
        inner_frame.pack(padx=20, pady=20)

        # Entry fields with modern styling
        fields = [
            ("Amount", 0),
            ("Category", 1),
            ("Date (YYYY-MM-DD)", 2)
        ]

        self.entries = {}
        
        for label_text, col in fields:
            # Label
            label = tk.Label(inner_frame, 
                           text=label_text,
                           font=('Segoe UI', 10),
                           bg="white",
                           fg=self.colors["secondary"])
            label.grid(row=0, column=col, padx=10, sticky="w")
            
            # Entry with custom style
            entry = tk.Entry(inner_frame,
                           font=('Segoe UI', 11),
                           relief="solid",
                           bd=1,
                           highlightthickness=2,
                           highlightbackground=self.colors["border"],
                           highlightcolor=self.colors["primary"])
            entry.grid(row=1, column=col, padx=10, pady=(5, 0), ipady=8, ipadx=5, sticky="ew")
            
            # Store entries
            if "Amount" in label_text:
                self.amount_entry = entry
            elif "Category" in label_text:
                self.category_entry = entry
            else:
                self.date_entry = entry
                self.date_entry.insert(0, datetime.date.today())

        # Add button with modern styling
        add_button = tk.Button(inner_frame,
                              text="Add Expense",
                              command=self.add_expense,
                              font=('Segoe UI', 11, 'bold'),
                              bg=self.colors["success"],
                              fg="white",
                              relief="flat",
                              cursor="hand2",
                              padx=20,
                              pady=10)
        add_button.grid(row=1, column=3, padx=10, sticky="ew")
        
        # Hover effects
        add_button.bind("<Enter>", lambda e: add_button.config(bg="#059669"))
        add_button.bind("<Leave>", lambda e: add_button.config(bg=self.colors["success"]))

        # Configure grid weights
        for i in range(4):
            inner_frame.columnconfigure(i, weight=1)

        # Expenses list section
        list_frame = tk.Frame(main_container, bg="white", relief="flat")
        list_frame.pack(fill="both", expand=True)
        list_frame.configure(highlightbackground=self.colors["border"], 
                           highlightthickness=1)

        # Section header
        list_header = tk.Frame(list_frame, bg="white")
        list_header.pack(fill="x", padx=20, pady=(15, 10))
        
        tk.Label(list_header,
                text="Recent Expenses",
                font=('Segoe UI', 14, 'bold'),
                bg="white",
                fg=self.colors["dark"]).pack(side="left")
        
        # Delete button
        delete_button = tk.Button(list_header,
                                 text="Delete Selected",
                                 command=self.delete_expense,
                                 font=('Segoe UI', 9),
                                 bg=self.colors["danger"],
                                 fg="white",
                                 relief="flat",
                                 cursor="hand2",
                                 padx=15,
                                 pady=5)
        delete_button.pack(side="right")
        delete_button.bind("<Enter>", lambda e: delete_button.config(bg="#dc2626"))
        delete_button.bind("<Leave>", lambda e: delete_button.config(bg=self.colors["danger"]))

        # Treeview with scrollbar
        tree_container = tk.Frame(list_frame, bg="white")
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        scrollbar = ttk.Scrollbar(tree_container)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_container,
                                columns=("Date", "Category", "Amount"),
                                show="headings",
                                yscrollcommand=scrollbar.set)
        
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount ($)")
        
        self.tree.column("Date", width=150, anchor="center")
        self.tree.column("Category", width=200, anchor="w")
        self.tree.column("Amount", width=150, anchor="e")
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

        # Bottom buttons
        button_frame = tk.Frame(main_container, bg="#f0f0f0")
        button_frame.pack(fill="x", pady=(20, 0))

        analytics_button = tk.Button(button_frame,
                                    text="📊 Show Analytics",
                                    command=self.show_analytics,
                                    font=('Segoe UI', 11, 'bold'),
                                    bg=self.colors["primary"],
                                    fg="white",
                                    relief="flat",
                                    cursor="hand2",
                                    padx=30,
                                    pady=12)
        analytics_button.pack(side="left", expand=True, fill="x", padx=(0, 10))
        analytics_button.bind("<Enter>", lambda e: analytics_button.config(bg="#1d4ed8"))
        analytics_button.bind("<Leave>", lambda e: analytics_button.config(bg=self.colors["primary"]))

        summary_button = tk.Button(button_frame,
                                  text="💵 Show Summary",
                                  command=self.show_summary,
                                  font=('Segoe UI', 11, 'bold'),
                                  bg=self.colors["secondary"],
                                  fg="white",
                                  relief="flat",
                                  cursor="hand2",
                                  padx=30,
                                  pady=12)
        summary_button.pack(side="left", expand=True, fill="x")
        summary_button.bind("<Enter>", lambda e: summary_button.config(bg="#475569"))
        summary_button.bind("<Leave>", lambda e: summary_button.config(bg=self.colors["secondary"]))

    def add_expense(self):
        amount = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        date = self.date_entry.get().strip()

        if not amount or not category or not date:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            float_amount = float(amount)
            if float_amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number")
            return

        # Validate date format
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format")
            return

        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount])

        self.tree.insert("", 0, values=(date, category, f"${float(amount):.2f}"))
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", "Expense added successfully!")

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?"):
            # Get all expenses
            expenses = []
            with open(FILE_NAME, "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                expenses = list(reader)
            
            # Remove selected expense
            for item in selected:
                values = self.tree.item(item)['values']
                # Remove $ and convert back
                amount = str(values[2]).replace('$', '')
                expenses = [e for e in expenses if not (e[0] == values[0] and e[1] == values[1] and e[2] == amount)]
                self.tree.delete(item)
            
            # Write back
            with open(FILE_NAME, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(expenses)

    def load_expenses(self):
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                date, category, amount = row
                self.tree.insert("", "end", values=(date, category, f"${float(amount):.2f}"))

    def show_summary(self):
        total = 0
        count = 0
        
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                total += float(row[2])
                count += 1
        
        if count == 0:
            messagebox.showinfo("Summary", "No expenses recorded yet")
            return
        
        avg = total / count
        message = f"Total Expenses: ${total:.2f}\n"
        message += f"Number of Expenses: {count}\n"
        message += f"Average Expense: ${avg:.2f}"
        
        messagebox.showinfo("Expense Summary", message)

    def show_analytics(self):
        categories = {}

        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                _, category, amount = row
                categories[category] = categories.get(category, 0) + float(amount)

        if not categories:
            messagebox.showinfo("No Data", "No expenses to analyze")
            return

        # Create a new window for the chart
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Spending Analytics")
        chart_window.geometry("800x600")
        chart_window.configure(bg="white")

        # Create matplotlib figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.patch.set_facecolor('white')
        
        # Pie chart
        colors_list = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
        ax1.pie(categories.values(), labels=categories.keys(), autopct="%1.1f%%",
               colors=colors_list, startangle=90)
        ax1.set_title("Spending by Category", fontsize=14, fontweight='bold', pad=20)
        
        # Bar chart
        bars = ax2.bar(categories.keys(), categories.values(), color=colors_list[:len(categories)])
        ax2.set_title("Category Comparison", fontsize=14, fontweight='bold', pad=20)
        ax2.set_ylabel("Amount ($)", fontsize=11)
        ax2.set_xlabel("Category", fontsize=11)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:.2f}',
                    ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()