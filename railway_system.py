import mysql.connector

# --- Database Connection Function ---
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",            # change if needed
        password="sql.sql", # your MySQL password
        database="mydb"
    )

# --- 1. Search Trains ---
def sp_search_trains():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        source = input("Enter source station: ")
        destination = input("Enter destination station: ")

        query = "SELECT train_id, train_name, fare FROM trains WHERE source=%s AND destination=%s"
        cursor.execute(query, (source, destination))
        results = cursor.fetchall()

        if results:
            print("\nAvailable trains:")
            for row in results:
                print(f"Train ID: {row[0]}, Name: {row[1]}, Fare: {row[2]}")
        else:
            print("No trains found for this route.")

    except Exception as e:
        print("❌ Error:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# --- 2. Book Ticket ---
def sp_book_ticket():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        passenger = input("Enter passenger name: ")
        train_id = input("Enter train ID to book: ")

        query = "INSERT INTO tickets (train_id, passenger_name, status) VALUES (%s, %s, %s)"
        cursor.execute(query, (train_id, passenger, "BOOKED"))
        conn.commit()

        print("✅ Ticket booked successfully!")

    except Exception as e:
        print("❌ Error:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# --- 3. Cancel Ticket ---
def sp_cancel_ticket():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        ticket_id = input("Enter ticket ID to cancel: ")

        query = "UPDATE tickets SET status=%s WHERE ticket_id=%s"
        cursor.execute(query, ("CANCELLED", ticket_id))
        conn.commit()

        if cursor.rowcount > 0:
            print("✅ Ticket cancelled successfully!")
        else:
            print("⚠️ Ticket not found.")

    except Exception as e:
        print("❌ Error:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# --- 4. Check Fare ---
def check_fare():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        train_id = input("Enter train ID: ")

        query = "SELECT fare FROM trains WHERE train_id=%s"
        cursor.execute(query, (train_id,))
        result = cursor.fetchone()

        if result:
            print(f"💰 Fare for train {train_id}: {result[0]}")
        else:
            print("⚠️ Train not found.")

    except Exception as e:
        print("❌ Error:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# --- Main Menu ---
def main_menu():
    while True:
        print("\n--- Railway Management ---")
        print("1. Search Trains")
        print("2. Book Ticket")
        print("3. Cancel Ticket")
        print("4. Check Fare")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            sp_search_trains()
        elif choice == "2":
            sp_book_ticket()
        elif choice == "3":
            sp_cancel_ticket()
        elif choice == "4":
            check_fare()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Try again.")

# Run program
main_menu()
