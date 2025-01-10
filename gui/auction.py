import tkinter as tk
from tkinter import ttk, messagebox
import cx_Oracle

# Database connection
dsn = cx_Oracle.makedsn(
    host="oracle.scs.ryerson.ca",
    port=1521,
    sid="orcl"
)

conn = cx_Oracle.connect(
    user="m3kashif",
    password="xxxx",
    dsn=dsn
)
cur = conn.cursor()

# Helper Functions
def execute_query(query, params=None, fetch=True):
    """Executes a SQL query with optional parameters and fetch results."""
    try:
        cur.execute(query, params or {})
        if fetch:
            return cur.fetchall(), [desc[0] for desc in cur.description]
        else:
            conn.commit()
            messagebox.showinfo("Success", "Operation completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None, None

def display_table_data(table_name):
    """Displays data from a specific table."""
    query = f"SELECT * FROM {table_name}"
    rows, columns = execute_query(query)
    if rows is not None:
        result_window = tk.Toplevel(root)
        result_window.title(f"{table_name} Data")
        result_window.configure(bg="#f9f9f9")
        tk.Label(result_window, text=f"{table_name} Data", font=("Helvetica", 16, "bold"), bg="#f9f9f9").pack(pady=10)
        tree = ttk.Treeview(result_window, style="Custom.Treeview")
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for row in rows:
            tree.insert("", "end", values=row)

def search_car():
    """Search for a car based on its name."""
    search_window = tk.Toplevel(root)
    search_window.title("Search Car")
    search_window.configure(bg="#f9f9f9")
    tk.Label(search_window, text="Search for a Car", font=("Helvetica", 16, "bold"), bg="#f9f9f9").pack(pady=10)
    tk.Label(search_window, text="Enter Car Name:", font=("Helvetica", 12), bg="#f9f9f9").pack(pady=5)
    car_name_var = tk.StringVar()
    tk.Entry(search_window, textvariable=car_name_var, width=30, font=("Helvetica", 12)).pack(pady=5)

    def perform_search():
        car_name = car_name_var.get()
        if not car_name:
            messagebox.showwarning("Warning", "Please enter a car name.")
            return

        query = "SELECT * FROM Cars WHERE LOWER(Make) LIKE :car_name OR LOWER(Model) LIKE :car_name"
        rows, columns = execute_query(query, params={"car_name": f"%{car_name.lower()}%"})
        if rows:
            result_window = tk.Toplevel(search_window)
            result_window.title(f"Search Results for '{car_name}'")
            result_window.configure(bg="#f9f9f9")
            tk.Label(result_window, text=f"Search Results for '{car_name}'", font=("Helvetica", 16, "bold"), bg="#f9f9f9").pack(pady=10)
            tree = ttk.Treeview(result_window, style="Custom.Treeview")
            tree.pack(expand=True, fill="both", padx=10, pady=10)
            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            for row in rows:
                tree.insert("", "end", values=row)
        else:
            messagebox.showinfo("No Results", f"No cars found matching '{car_name}'.")

    tk.Button(search_window, text="Search", command=perform_search, bg="#0078d7", fg="white", font=("Helvetica", 12), width=10).pack(pady=10)

def add_record():
    """Window to add a record with field-by-field inputs."""
    add_window = tk.Toplevel(root)
    add_window.title("Add Record")
    add_window.configure(bg="#f9f9f9")
    tk.Label(add_window, text="Select Table to Add Record", font=("Helvetica", 16, "bold"), bg="#f9f9f9").pack(pady=10)
    table_var = tk.StringVar()
    table_dropdown = ttk.Combobox(add_window, textvariable=table_var, font=("Helvetica", 12), width=30)
    table_dropdown["values"] = ["Users", "Cars"]
    table_dropdown.pack(pady=5)

    def next_step():
        table = table_var.get()
        if not table:
            messagebox.showwarning("Warning", "Please select a table.")
            return

        # Clear previous widgets
        for widget in add_window.winfo_children():
            widget.destroy()

        if table == "Users":
            add_user(add_window)
        elif table == "Cars":
            add_car(add_window)

    tk.Button(add_window, text="Next", command=next_step, bg="#0078d7", fg="white", font=("Helvetica", 12), width=10).pack(pady=10)

def add_user(window):
    """Add a new user record."""
    window.configure(bg="#f9f9f9")
    tk.Label(window, text="Enter User Details", font=("Helvetica", 16, "bold"), bg="#f9f9f9").pack(pady=10)
    fields = {"UserID": tk.StringVar(), "Username": tk.StringVar(), "Password": tk.StringVar(), 
              "Email": tk.StringVar(), "Role (0=Buyer, 1=Seller)": tk.StringVar()}
    for label, var in fields.items():
        tk.Label(window, text=label, font=("Helvetica", 12), bg="#f9f9f9").pack(pady=5)
        tk.Entry(window, textvariable=var, font=("Helvetica", 12), width=30).pack(pady=5)

    def submit():
        try:
            cur.execute(
                "INSERT INTO Users (UserID, Username, Password, Email, Role) VALUES (:1, :2, :3, :4, :5)",
                (fields["UserID"].get(), fields["Username"].get(), fields["Password"].get(),
                 fields["Email"].get(), fields["Role (0=Buyer, 1=Seller)"].get())
            )
            conn.commit()
            messagebox.showinfo("Success", "User added successfully!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(window, text="Submit", command=submit, bg="#0078d7", fg="white", font=("Helvetica", 12), width=10).pack(pady=10)

def add_car(window):
    """Add a new car record."""
    window.configure(bg="#f9f9f9")
    tk.Label(window, text="Enter Car Details", font=("Helvetica", 16, "bold"), bg="#f9f9f9").pack(pady=10)
    fields = {
        "CarID": tk.StringVar(),
        "Make": tk.StringVar(),
        "Model": tk.StringVar(),
        "Year": tk.StringVar(),
        "Color": tk.StringVar(),
        "Mileage": tk.StringVar()
    }
    for label, var in fields.items():
        tk.Label(window, text=label, font=("Helvetica", 12), bg="#f9f9f9").pack(pady=5)
        tk.Entry(window, textvariable=var, font=("Helvetica", 12), width=30).pack(pady=5)

    def submit():
        try:
            cur.execute(
                "INSERT INTO Cars (CarID, Make, Model, Year, Color, Mileage) VALUES (:1, :2, :3, :4, :5, :6)",
                (fields["CarID"].get(), fields["Make"].get(), fields["Model"].get(),
                 fields["Year"].get(), fields["Color"].get(), fields["Mileage"].get())
            )
            conn.commit()
            messagebox.showinfo("Success", "Car added successfully!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(window, text="Submit", command=submit, bg="#0078d7", fg="white", font=("Helvetica", 12), width=10).pack(pady=10)

# GUI Setup
root = tk.Tk()
root.title("Car Auction DB Management")
root.configure(bg="#f9f9f9")

# Custom Treeview Style
style = ttk.Style()
style.configure("Custom.Treeview", background="#f9f9f9", foreground="black", rowheight=25, font=("Helvetica", 10))
style.configure("Custom.Treeview.Heading", font=("Helvetica", 12, "bold"), background="#0078d7", foreground="black")

tk.Label(root, text="Car Auction Database Management", font=("Helvetica", 20, "bold"), bg="#f9f9f9", fg="#0078d7").pack(pady=20)
tk.Button(root, text="Display Users Table", command=lambda: display_table_data("Users"), bg="#0078d7", fg="white", font=("Helvetica", 12), width=20).pack(pady=5)
tk.Button(root, text="Display Bids Table", command=lambda: display_table_data("Bids"), bg="#0078d7", fg="white", font=("Helvetica", 12), width=20).pack(pady=5)
tk.Button(root, text="Display Auction Table", command=lambda: display_table_data("Auction"), bg="#0078d7", fg="white", font=("Helvetica", 12), width=20).pack(pady=5)
tk.Button(root, text="Display Cars Table", command=lambda: display_table_data("Cars"), bg="#0078d7", fg="white", font=("Helvetica", 12), width=20).pack(pady=5)
tk.Button(root, text="Search Car", command=search_car, bg="#0078d7", fg="white", font=("Helvetica", 12), width=20).pack(pady=5)
tk.Button(root, text="Add Record", command=add_record, bg="#0078d7", fg="white", font=("Helvetica", 12), width=20).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit, bg="#d9534f", fg="white", font=("Helvetica", 12), width=20).pack(pady=10)
tk.Button(root, text="Drop Table", command=drop_table, bg="#d9534f", fg="white", font=("Helvetica", 12), width=20).pack(pady=5)

root.mainloop()

# Cleanup
cur.close()
conn.close()
