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
    cursor.execute('''CREATE TABLE IF NOT EXISTS games (
                        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_name TEXT NOT NULL,
                        item_description TEXT,
                        platform TEXT,
                        release_date TEXT
                      )''')
    if DEBUG_MODE:
        print("Table Created")  
    conn.commit()
    return conn 

# View an item
def view_items():
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games")
    items = cursor.fetchall()
    conn.close()
    return items

# Add an item
def add_item(item_name, item_description, platform, release_date):
    if DEBUG_MODE:
        print("Started Connection")
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO games (item_name, item_description, platform, release_date) VALUES (?, ?, ?, ?)",  
                   (item_name, item_description, platform, release_date))
    conn.commit()
    conn.close()
    print("Item added successfully.")

# Edit an item
def edit_item(item_id, item_name=None, item_description=None, platform=None, release_date=None):
    conn = conn_db()
    cursor = conn.cursor()
    updates = []
    values = []

    if item_name:
        updates.append("item_name = ?")
        values.append(item_name)
    if item_description:
        updates.append("item_description = ?")
        values.append(item_description)
    if platform:
        updates.append("platform = ?")
        values.append(platform)
    if release_date:
        updates.append("release_date = ?")
        values.append(release_date)
    
    values.append(item_id)
    query = f"UPDATE games SET {', '.join(updates)} WHERE item_id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    print("Item updated successfully.")

# Remove an item
def remove_item(item_id):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM games WHERE item_id = ?", (item_id,))
    conn.commit() 
    conn.close()
    print("Item removed successfully.")

# Example usage
if __name__ == "__main__":
    conn_db()  # Create database and table
    print("Viewing items:")
    print(view_items())  # Initially empty

    add_item("FIFA 22", "Football simulation game", "PlayStation", "2021-09-27")
    print("After adding an item:")
    print(view_items())  # Should show the newly added item
