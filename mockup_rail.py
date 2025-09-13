def sp_search_trains():
    print("🔍 Searching trains...")

def sp_book_ticket():
    print("🎟️ Booking ticket...")

def sp_cancel_ticket():
    print("❌ Cancelling ticket...")

def check_fare():
    print("💰 Checking fare...")

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
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# run menu
main_menu()


            