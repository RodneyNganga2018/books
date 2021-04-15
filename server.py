from flask import Flask, request, redirect, render_template
from mysqlconnection import connectToMySQL
app = Flask (__name__)

@app.route('/authors')
def index():
    authors_db = connectToMySQL('books_schema').query_db('SELECT name, id FROM authors;')
    return render_template('index.html', authors_tp=authors_db)

@app.route('/authors/new', methods=['POST'])
def add_author():
    query = 'INSERT INTO authors(name) VALUES(%(author_name)s);'
    data = {
        'author_name': request.form['author_name']
    }
    connectToMySQL('books_schema').query_db(query,data)
    return redirect('/authors')

@app.route('/books')
def books():
    books_db = connectToMySQL('books_schema').query_db('SELECT title, id FROM books;')
    return render_template('books.html', books_tp=books_db)

@app.route('/books/new', methods=['POST'])
def add_book():
    query = 'INSERT INTO books(title,num_of_pages) VALUES(%(title)s,%(pages)s);'
    data = {
        'title': request.form['title'],
        'pages': request.form['pages']
    }
    connectToMySQL('books_schema').query_db(query,data)
    return redirect('/books')

@app.route('/authors/<author_id>')
def author(author_id):
    data = {
        'author_id': author_id
    }
    favorite_book_db = connectToMySQL('books_schema').query_db('SELECT authors.id,authors.name,books.title as title,books.num_of_pages as pages FROM authors LEFT JOIN favorites ON authors.id=favorites.author_id LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id=%(author_id)s;',data)
    books_db = connectToMySQL('books_schema').query_db('SELECT title, id FROM books;')
    fav_books_db = []
    for book in favorite_book_db:
        fav_books_db.append(book['title'])
    return render_template("author.html", favorite_book_tp=favorite_book_db, fav_book_tp=fav_books_db, books_tp=books_db)

@app.route('/authors/<author_id>/new_fav', methods=['POST'])
def add_favbook(author_id):
    data = {
        'author_id': author_id,
        'book_id': request.form['book']
    }
    connectToMySQL('books_schema').query_db('INSERT INTO favorites(author_id,book_id) VALUES(%(author_id)s,%(book_id)s);',data)
    return redirect('/authors/'+author_id)

@app.route('/books/<book_id>')
def book(book_id):
    data = {
        'book_id': book_id
    }
    favorite_author_db = connectToMySQL('books_schema').query_db('SELECT authors.name as name,books.id,books.title FROM books LEFT JOIN favorites ON books.id=favorites.book_id LEFT JOIN authors ON favorites.author_id=authors.id WHERE books.id=%(book_id)s;',data)
    authors_db = connectToMySQL('books_schema').query_db('SELECT name, id FROM authors;')
    fav_authors_db = []
    for author in favorite_author_db:
        fav_authors_db.append(author['name'])
    return render_template('book.html', favorite_author_tp=favorite_author_db, fav_author_tp=fav_authors_db, authors_tp=authors_db)

@app.route('/books/<book_id>/new_fav', methods=['POST'])
def add_favauthor(book_id):
    data = {
        'author_id': request.form['author'],
        'book_id': book_id
    }
    connectToMySQL('books_schema').query_db('INSERT INTO favorites(author_id,book_id) VALUES(%(author_id)s,%(book_id)s);',data)
    return redirect('/books/'+book_id)

if __name__ == '__main__':
    app.run(debug=True)