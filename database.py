# database.py
import os
import psycopg2
from psycopg2.extras import DictCursor

# Get the database connection URL from an environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db():
    """Connects to the PostgreSQL database."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    """Initializes the database tables if they don't exist."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                bank TEXT NOT NULL
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS benefits (
                id SERIAL PRIMARY KEY,
                card_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                FOREIGN KEY (card_id) REFERENCES cards (id)
            );
        ''')
    db.commit()
    db.close()

def add_card(name, bank):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO cards (name, bank) VALUES (%s, %s)", (name, bank))
    db.commit()
    db.close()

def add_benefit(card_id, description, category):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO benefits (card_id, description, category) VALUES (%s, %s, %s)",
                       (card_id, description, category))
    db.commit()
    db.close()

def get_all_cards():
    db = get_db()
    with db.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('SELECT * FROM cards')
        cards = cursor.fetchall()
    db.close()
    return cards

def get_card_and_benefits(card_id):
    db = get_db()
    with db.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('SELECT * FROM cards WHERE id = %s', (card_id,))
        card = cursor.fetchone()
        cursor.execute('SELECT * FROM benefits WHERE card_id = %s', (card_id,))
        benefits = cursor.fetchall()
    db.close()
    return card, benefits
