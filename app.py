from flask import Flask, render_template, request
from models import db, Book
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    books = Book.query.filter(
        (Book.title.ilike(f"%{query}%")) | (Book.author.ilike(f"%{query}%"))
    ).all()
    return render_template('search.html', books=books, query=query)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
