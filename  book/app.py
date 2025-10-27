from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="book1_db"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def home():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return render_template('books.html', books=books)

@app.route('/api/books', methods=['GET'])
def get_books():
    cursor.execute("SELECT * FROM books")
    return jsonify(cursor.fetchall())

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5011)
