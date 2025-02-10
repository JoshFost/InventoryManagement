import sqlite3
DEBUG_MODE = False

# Database connection setup

class DatabaseManager:
    def __init__(self, db_name, debug_mode=False):
        self.db_name = db_name
        self.debug_mode = debug_mode
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS customer (
                        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_first_name TEXT NOT NULL,
                        customer_middle_name TEXT,
                        customer_last_name TEXT NOT NULL,
                        customer_email_address TEXT NOT NULL
                      )''')
        self.conn.commit()

    def view_customers(self):
        """Retrieve all customers from the database and return as a list of tuples."""
        self.cursor.execute("SELECT * FROM customer")
        customers = self.cursor.fetchall()

        if self.debug_mode:
            print("Retrieved customers:", customers)

        return customers

    def add_customer(self, first_name, middle_name, last_name, email):
        """Adds a new customer to the database."""
        self.cursor.execute(
            "INSERT INTO customer (customer_first_name, customer_middle_name, customer_last_name, customer_email_address) VALUES (?, ?, ?, ?)",
            (first_name, middle_name, last_name, email),
        )
        self.conn.commit()

        if self.debug_mode:
            print(f"Customer {first_name} {last_name} added successfully.")
    def edit_customer(self, customer_id, first_name=None, middle_name=None, last_name=None, email=None):
        """Edits an existing customer based on provided fields."""
        updates = []
        values = []

        if first_name:
            updates.append("customer_first_name = ?")
            values.append(first_name)
        if middle_name:
            updates.append("customer_middle_name = ?")
            values.append(middle_name)
        if last_name:
            updates.append("customer_last_name = ?")
            values.append(last_name)
        if email:
            updates.append("customer_email_address = ?")
            values.append(email)

        if not updates:
            print("No updates provided.")
            return

        values.append(customer_id)
        query = f"UPDATE customer SET {', '.join(updates)} WHERE customer_id = ?"
        self.cursor.execute(query, values)
        self.conn.commit()

        if self.debug_mode:
            print(f"Customer ID {customer_id} updated successfully.")

    def remove_customer(self, customer_id):
        """Removes a customer from the database by ID."""
        self.cursor.execute("DELETE FROM customer WHERE customer_id = ?", (customer_id,))
        self.conn.commit()

        if self.debug_mode:
            print(f"Customer ID {customer_id} removed successfully.")

    def close(self):
        """Closes the database connection."""
        self.conn.close()

if __name__ == "__main__":
    # Initialize database
    db = DatabaseManager("inventory.db", debug_mode=True)  # Debug mode ON

    # Ensure table exists
    db.create_table()

    # Add a test customer
    db.add_customer("John", "A", "Doe", "john.doe@example.com")

    # View customers (before editing/removal)
    print("\n📌 Customers Before Editing/Removing:")
    for customer in db.view_customers():
        print(customer)

    # Edit the customer (assuming ID is 1)
    db.edit_customer(1, first_name="Jonathan", email="jonathan.doe@example.com")

    # View customers (after editing)
   # print("\n✏️ Customers After Editing:")
    #for customer in db.view_customers():
     #   print(customer)

    # Remove the customer (assuming ID is 1)
    #db.remove_customer(1)

    # View customers (after removal)
    #print("\n❌ Customers After Removal:")
    #for customer in db.view_customers():
     #   print(customer)

    # Close database connection
    #db.close()
    #print("\n🔒 Database connection closed.")