# database.py
import sqlite3
import os

# Render's disk will be mounted at this directory.
# We default to the current directory for local development.
DATA_DIR = os.environ.get('RENDER_DISK_PATH', '.')
DATABASE_NAME = os.path.join(DATA_DIR, 'cards.db')

def get_db():
    """Connects to the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database tables if they don't exist."""
    # Create the data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bank TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS benefits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            FOREIGN KEY (card_id) REFERENCES cards (id)
        );
    ''')
    db.commit()
    db.close()

# --- The rest of your functions (add_card, add_benefit) stay exactly the same ---
def add_card(name, bank):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO cards (name, bank) VALUES (?, ?)", (name, bank))
    db.commit()
    db.close()

def add_benefit(card_id, description, category):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO benefits (card_id, description, category) VALUES (?, ?, ?)",
                   (card_id, description, category))
    db.commit()
    db.close()

if __name__ == '__main__':
    init_db()
    print(f"Database initialized at {DATABASE_NAME}")
