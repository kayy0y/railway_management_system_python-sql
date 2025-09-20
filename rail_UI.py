import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import mysql.connector

# --- Database Connection Helper ---
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # change if needed
        password="sql.sql",  # update with your password
        database="mydb"
    )

class RailwayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚆 Railway Management System")
        self.root.geometry("750x500")
        self.root.config(bg="#f0f4f7")

        # Apply ttk theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 12), padding=6)
        style.configure("TLabel", font=("Arial", 12), background="#f0f4f7")

        # Title
        title_label = tk.Label(
            root, text="Railway Management System",
            font=("Arial", 20, "bold"), bg="#2c3e50", fg="white", pady=10
        )
        title_label.pack(fill="x")

        # Buttons menu
        menu_frame = tk.Frame(root, bg="#f0f4f7")
        menu_frame.pack(side="left", fill="y", padx=20, pady=20)

        ttk.Button(menu_frame, text="Search Trains", width=20, command=self.search_trains).pack(pady=10)
        ttk.Button(menu_frame, text="Book Ticket", width=20, command=self.book_ticket).pack(pady=10)
        ttk.Button(menu_frame, text="Cancel Ticket", width=20, command=self.cancel_ticket).pack(pady=10)
        ttk.Button(menu_frame, text="Check Fare", width=20, command=self.check_fare).pack(pady=10)
        ttk.Button(menu_frame, text="Exit", width=20, command=root.quit).pack(pady=10)

        # Output area (Treeview for results)
        output_frame = tk.Frame(root, bg="#f0f4f7")
        output_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        tk.Label(output_frame, text="Output:", font=("Arial", 14, "bold"), bg="#f0f4f7").pack(anchor="w")

        columns = ("Train ID", "Train Name", "Fare")
        self.tree = ttk.Treeview(output_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)

    def clear_output(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def search_trains(self):
        source = simpledialog.askstring("Search Trains", "Enter source station:")
        destination = simpledialog.askstring("Search Trains", "Enter destination station:")
        if not source or not destination:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT train_id, train_name, fare FROM trains WHERE source=%s AND destination=%s"
            cursor.execute(query, (source, destination))
            results = cursor.fetchall()
            self.clear_output()
            if results:
                for row in results:
                    self.tree.insert("", "end", values=row)
            else:
                messagebox.showinfo("No Results", "No trains found for this route.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def book_ticket(self):
        passenger = simpledialog.askstring("Book Ticket", "Enter passenger name:")
        train_id = simpledialog.askstring("Book Ticket", "Enter train ID:")
        if not passenger or not train_id:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT train_name FROM trains WHERE train_id=%s", (train_id,))
            train = cursor.fetchone()
            if not train:
                messagebox.showwarning("Invalid", "Train ID not found.")
                return
            query = "INSERT INTO tickets (train_id, passenger_name, status) VALUES (%s, %s, %s)"
            cursor.execute(query, (train_id, passenger, "BOOKED"))
            conn.commit()
            messagebox.showinfo("Success", f"Ticket booked for {passenger} on {train[0]}!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def cancel_ticket(self):
        ticket_id = simpledialog.askstring("Cancel Ticket", "Enter ticket ID:")
        if not ticket_id:
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "UPDATE tickets SET status=%s WHERE ticket_id=%s"
            cursor.execute(query, ("CANCELLED", ticket_id))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Ticket cancelled successfully!")
            else:
                messagebox.showwarning("Not Found", "Ticket ID not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def check_fare(self):
        train_id = simpledialog.askstring("Check Fare", "Enter train ID:")
        if not train_id:
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT fare FROM trains WHERE train_id=%s"
            cursor.execute(query, (train_id,))
            result = cursor.fetchone()
            if result:
                messagebox.showinfo("Fare", f"Fare for train {train_id}: ₹{result[0]}")
            else:
                messagebox.showwarning("Not Found", "Train ID not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = RailwayApp(root)
    root.mainloop()

