from flask import Flask, render_template, request, jsonify
import mysql.connector
import requests
from datetime import datetime

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="order1_db"
)
cursor = db.cursor(dictionary=True)


BOOK_SERVICE_URL = "http://127.0.0.1:5011"

@app.route('/order/<int:book_id>')
def order_page(book_id):
    try:
        res = requests.get(f"{BOOK_SERVICE_URL}/api/books/{book_id}")
        res.raise_for_status()
    except Exception as e:
        return f"Error connecting to Book Service: {e}", 500

    book = res.json()
    if 'error' in book:
        return "Book not found", 404

    return render_template('order.html', book=book)

@app.route('/place_order', methods=['POST'])
def place_order():
    book_id = request.form['book_id']
    customer_name = request.form['customer_name']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    total_price = price * quantity
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("""
        INSERT INTO orders (book_id, customer_name, quantity, total_price, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (book_id, customer_name, quantity, total_price, created_at))
    db.commit()

    return render_template('success.html', name=customer_name, total=total_price)

@app.route('/api/orders')
def api_orders():
    cursor.execute("SELECT * FROM orders")
    return jsonify(cursor.fetchall())

if __name__ == '__main__':
    app.run(debug=True, port=5005)
