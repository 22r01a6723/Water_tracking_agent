import sqlite3
from datetime import datetime

DB_NAME ="water_tracker.db"

def create_tables():
    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS water_intake(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        intake_ml INTEGER,
        date TEXT
                   )""")
    
    conn.commit()
    conn.close()
def log_intake(user_id ,intake_ml):
    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()
    # convert user_id to string explicitly
    user_id_str = str(user_id)
    date_today=datetime.today().strftime('%Y-%m-%d')
    cursor.execute("INSERT INTO water_intake(user_id,intake_ml,date)VALUES(?,?,?)",(user_id_str,intake_ml,date_today))
    conn.commit()
    conn.close()    
    
    
def get_intake_history(user_id):
    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()
    # strip all quotes and whitespace to ensure clean matching
    user_id_str = str(user_id).strip().strip('"').strip("'")
    print(f"DEBUG: Querying with user_id='{user_id_str}' (type: {type(user_id_str)})")
    cursor.execute("SELECT intake_ml,date FROM water_intake WHERE CAST(user_id AS TEXT)=?",(user_id_str,))
    records=cursor.fetchall()
    print(f"DEBUG: Found {len(records)} records")
    conn.close()  
    return records
create_tables()
    
    
      
