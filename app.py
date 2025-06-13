from flask import Flask, render_template, request, redirect
import json
import uuid
import os

app = Flask(__name__)
BOOKS_FILE = 'books.json'

def load_books():
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, 'r') as f:
        return json.load(f)

def save_books(books):
    with open(BOOKS_FILE, 'w') as f:
        json.dump(books, f, indent=4)

@app.route('/')
def index():
    books = load_books()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add():
    books = load_books()
    books.append({
        'id': str(uuid.uuid4()),
        'title': request.form['title'],
        'author': request.form['author'],
        'price': request.form['price']
    })
    save_books(books)
    return redirect('/')

@app.route('/delete/<id>')
def delete(id):
    books = load_books()
    books = [b for b in books if b['id'] != id]
    save_books(books)
    return redirect('/')

if __name__ == '__main__':
    app.run()
