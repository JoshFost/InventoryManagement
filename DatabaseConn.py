import sqlite3
DEBUG_MODE = False

# Database connection setup
def conn_db():
    if DEBUG_MODE:
        print("Started Connection")
    conn = sqlite3.connect("inventory.db")
    if DEBUG_MODE:
        print("Connection Established")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS customer (
                        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_first_name TEXT NOT NULL,
                        customer_middle_name TEXT,
                        customer_last_name TEXT NOT NULL,
                        customer_email_address TEXT NOT NULL
                      )''')
    if DEBUG_MODE:
        print("Table Created")  
    conn.commit()
    return conn 

# View an item
def view_items():
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer")
    items = cursor.fetchall()
    conn.close()
    return items

# Add an item
def add_item(customer_first_name, customer_middle_name, customer_last_name, customer_email_address):
    if DEBUG_MODE:
        print("Started Connection")
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customer (customer_first_name, customer_middle_name, customer_last_name, customer_email_address) VALUES (?, ?, ?, ?)",  
                   (customer_first_name, customer_middle_name, customer_last_name, customer_email_address))
    conn.commit()
    conn.close()
    print("customer added successfully.")

# Edit an item
def edit_item(customer_id, customer_first_name =None, customer_middle_name =None, customer_last_name=None, customer_email_address=None):
    conn = conn_db()
    cursor = conn.cursor()
    updates = []
    values = []

    if customer_first_name:
        updates.append("customer_first_name = ?")
        values.append(customer_first_name)
    if customer_middle_name:
        updates.append("customer_middle_name = ?")
        values.append(customer_middle_name)
    if customer_last_name:
        updates.append("customer_last_name = ?")
        values.append(customer_last_name)
    if customer_email_address:
        updates.append("customer_email_address = ?")
        values.append(customer_email_address)
    
    values.append(customer_id)
    query = f"UPDATE customer SET {', '.join(updates)} WHERE customer_id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    print("Item updated successfully.")

# Remove an item
def remove_item(customer_id):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customer WHERE customer_id = ?", (customer_id,))
    conn.commit() 
    conn.close()
    print("Item removed successfully.")

# Example usage
if __name__ == "__main__":
    conn_db()  # Ensure the table is created
    print("Table creation checked.")

    add_item("John", "A", "Doe", "john.doe@example.com")
    print("Added a customer.")

    print("Viewing customers:")
    print(view_items())  # This should now show at least one record
