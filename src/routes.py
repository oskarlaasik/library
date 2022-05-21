from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy import or_, func
from werkzeug.security import generate_password_hash, check_password_hash

from src import db
from src.forms import BookSearchForm, BookAddForm
from src.models import User, Book, Borrow

api_bp = Blueprint('api_bp', __name__)  # "API Blueprint"

client_bp = Blueprint('client_bp', __name__,  # 'Client Blueprint'
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/client/static'
                      )


@client_bp.route("/")
def index():
    return render_template("index.html")


@client_bp.route("/library")
@login_required
def library():
    return render_template("library.html", name=current_user.name)


@login_required
@client_bp.route('/books', methods=('GET', 'POST'))
def books():
    if not current_user.is_authenticated:
        return redirect(url_for('client_bp.index'))
    search = request.form.get('search')
    my_books = db.session.query(Book, Borrow.date_end)\
        .filter(Book.id == Borrow.book_id)\
        .filter(Borrow.active==True)

    if search:
        my_books = my_books.filter(
            or_(func.lower(Book.title).contains(search.lower()),
                func.lower(Book.genre).contains(search.lower()),
                func.lower(Book.author).contains(search.lower())
                ))
    my_books = my_books.order_by(Book.title.asc()).all()


    return render_template('books.html', books=my_books, form=BookSearchForm())


@login_required
@client_bp.route('/search')
def search():
    my_books = Book.query.filter(user=current_user.id).all()
    return render_template('books.html', books=my_books)


@client_bp.route('/login')
def login():
    return render_template('login.html')


@client_bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('client_bp.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('client_bp.library'))


@client_bp.route('/signup')
def signup():
    return render_template('signup.html')


@client_bp.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('client_bp.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@client_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('client_bp.index'))


@api_bp.route('/book/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('client_bp.books'))

@api_bp.route('/book/mark_borrowed/<int:book_id>', methods=['POST'])
@login_required
def mark_borrowed(book_id):
    book = Book.query.get_or_404(book_id)
    book.borrowed = False if book.borrowed else True
    db.session.commit()
    return redirect(url_for('client_bp.books'))

@api_bp.route('/book/mark_reserved/<int:book_id>', methods=['POST'])
@login_required
def mark_reserved(book_id):
    book = Book.query.get_or_404(book_id)
    book.reserved = False if book.reserved else True
    db.session.commit()
    return redirect(url_for('client_bp.books'))


@client_bp.route('/book/add')
@login_required
def create_book():
    return render_template('createBook.html', form=BookAddForm())


@login_required
@client_bp.route('/book/add', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('name')
    year = request.form.get('year')
    genre = request.form.get('genre')
    if None or '' in (title, author, year, genre):
        flash('All fields must be filled!')
        return redirect(url_for('client_bp.create_book'))  # if book metadata is invalid, reload the page
    try:
        year = int(year)
    except Exception:
        flash('Year field must be Integer!')
        return redirect(url_for('client_bp.create_book'))

    # All fields are valid, create book
    Book.create(title=title,
                author=author,
                year=year,
                genre=genre,
                user_id=current_user.id
                )
    return redirect(url_for('client_bp.books'))
