from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user

from src.models import Book
from src.utils import BookSearchForm, BookAddForm, book_search, query_to_dict

client_bp = Blueprint('client_bp', __name__,  # 'Client Blueprint'
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/client/static'
                      )


@client_bp.route("/")
def index():
    return render_template("index.html")


@client_bp.route("/borrowed")
@login_required
def borrowed():
    # join due dates to books and filter current user books
    book_query = Book.query.filter(Book.reader_id == current_user.id)
    return render_template('borrowed.html', books=book_query)



@client_bp.route('/books', methods=('GET', 'POST'))
@login_required
def books():
    search_str = request.form.get('search')
    # join due dates to books and filter current user books
    book_query = Book.query.filter(Book.owner_id == current_user.id)

    if search_str:
        book_query = book_search(search_str, book_query)
    book_dict = query_to_dict(book_query)
    return render_template('books.html', books=book_dict, search_form=BookSearchForm())


@client_bp.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    if not current_user.is_authenticated:
        return redirect(url_for('client_bp.index'))
    search_str = request.form.get('search')
    book_query = Book.query
    if search_str:
        # join due dates to books
        book_query = book_search(search_str, book_query)
    return render_template('search.html', books=book_query, search_form=BookSearchForm())



@client_bp.route('/create_book')
@login_required
def create_book():
    return render_template('createBook.html', form=BookAddForm())


@client_bp.route('/login')
def login():
    return render_template('login.html')


@client_bp.route('/signup')
def signup():
    return render_template('signup.html')
