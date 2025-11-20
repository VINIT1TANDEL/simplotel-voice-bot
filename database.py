import sqlite3

def init_db():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS rooms
                 (room_number INTEGER, type TEXT, price INTEGER, available INTEGER)''')
    
    # Check if table is empty, if so, seed some data
    c.execute('SELECT count(*) FROM rooms')
    if c.fetchone()[0] == 0:
        rooms = [
            (101, 'Deluxe', 5000, 1),     # 1 = Available
            (102, 'Standard', 3000, 1),
            (103, 'Suite', 10000, 0),     # 0 = Booked
            (104, 'Deluxe', 5000, 1),
            (105, 'Standard', 3000, 0)
        ]
        c.executemany('INSERT INTO rooms VALUES (?,?,?,?)', rooms)
        conn.commit()
        print("Database initialized with dummy data.")
        
    conn.close()

def get_hotel_status():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    
    # Get count and price of AVAILABLE rooms grouped by type
    c.execute("SELECT type, price, count(*) FROM rooms WHERE available=1 GROUP BY type")
    available_data = c.fetchall()
    conn.close()
    
    status_text = "Current Hotel Data (Real-time):\n"
    if not available_data:
        status_text += "No rooms are currently available.\n"
    else:
        for r_type, price, count in available_data:
            status_text += f"- {r_type} Room: {count} available at {price} INR/night\n"
            
    return status_text