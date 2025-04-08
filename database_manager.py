import sqlite3
import os
from datetime import datetime

# Define the path to the database
DB_PATH = os.path.join(os.path.dirname(__file__), 'tracked_songs.db')

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            song TEXT,
            artist TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_entry():
    song = input("Enter the song name: ")
    artist = input("Enter the artist name: ")
    timestamp = input("Enter the timestamp (format: YYYY-MM-DD HH:MM:SS): ")
    if not timestamp:
        print("Timestamp is required. Please try again.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO songs (song, artist, timestamp) VALUES (?, ?, ?)', (song, artist, timestamp))
    conn.commit()
    conn.close()
    print(f"Added entry: {song} by {artist} at {timestamp}")

def delete_entry():
    list_entries()
    entry_id = input("Enter the ID of the entry to delete: ")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM songs WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()
    print(f"Deleted entry with id: {entry_id}")

def update_entry():
    list_entries()
    entry_id = input("Enter the ID of the entry to update: ")
    
    song = input("Enter the new song name (leave blank to keep current): ")
    artist = input("Enter the new artist name (leave blank to keep current): ")
    timestamp = input("Enter the new timestamp (leave blank to keep current, format: YYYY-MM-DD HH:MM:SS): ")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if song:
        cursor.execute('UPDATE songs SET song = ? WHERE id = ?', (song, entry_id))
    if artist:
        cursor.execute('UPDATE songs SET artist = ? WHERE id = ?', (artist, entry_id))
    if timestamp:
        cursor.execute('UPDATE songs SET timestamp = ? WHERE id = ?', (timestamp, entry_id))
    conn.commit()
    conn.close()
    print(f"Updated entry with id: {entry_id}")

def list_entries(limit=25):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM songs ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()
    print("\nLast 25 entries:")
    for row in rows:
        print(row)

def main():
    create_table()
    while True:
        list_entries()
        print("\nOptions: ")
        print("1. Add entry")
        print("2. Delete entry")
        print("3. Update entry")
        print("4. Quit")
        
        choice = input("Enter your choice: ")
        if choice == '1':
            add_entry()
        elif choice == '2':
            delete_entry()
        elif choice == '3':
            update_entry()
        elif choice == '4':
            print("Quitting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()