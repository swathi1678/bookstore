from flask import Flask, render_template, request, redirect, url_for
from models import db, Book
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///books.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    books = Book.query.filter(
        (Book.title.ilike(f"%{query}%")) | 
        (Book.author.ilike(f"%{query}%"))
    ).all()
    return render_template('search.html', books=books, query=query)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book = Book(
            title=request.form['title'],
            author=request.form['author'],
            price=float(request.form['price']),
            available='available' in request.form,
            description=request.form['description']
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)