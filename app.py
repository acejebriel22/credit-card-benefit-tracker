# app.py
from flask import Flask, render_template, request, redirect, url_for
import database as db

app = Flask(__name__)

# Route for the home page - shows all cards
@app.route('/')
def index():
    conn = db.get_db()
    cards = conn.execute('SELECT * FROM cards').fetchall()
    conn.close()
    return render_template('index.html', cards=cards)

# Route to show details for a single card
@app.route('/card/<int:card_id>')
def card_detail(card_id):
    conn = db.get_db()
    card = conn.execute('SELECT * FROM cards WHERE id = ?', (card_id,)).fetchone()
    benefits = conn.execute('SELECT * FROM benefits WHERE card_id = ?', (card_id,)).fetchall()
    conn.close()
    return render_template('card_detail.html', card=card, benefits=benefits)

# Route to handle adding a new card
@app.route('/add_card', methods=['POST'])
def add_card():
    name = request.form['name']
    bank = request.form['bank']
    db.add_card(name, bank)
    return redirect(url_for('index'))

# Route to handle adding a new benefit
@app.route('/card/<int:card_id>/add_benefit', methods=['POST'])
def add_benefit(card_id):
    description = request.form['description']
    category = request.form['category']
    db.add_benefit(card_id, description, category)
    return redirect(url_for('card_detail', card_id=card_id))

if __name__ == '__main__':
    # Initialize the database if it doesn't exist
    db.init_db()
    # Run the Flask app
    app.run(debug=True) # debug=True lets you see errors and auto-reloads
