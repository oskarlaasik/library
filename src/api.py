import datetime

from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from src import db
from src.models import Book, User

api_bp = Blueprint('api_bp', __name__)  # "API Blueprint"


@api_bp.route('/book/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('client_bp.books'))


@api_bp.route('/book/update_status/<int:book_id>/<string:status>', methods=['POST'])
@login_required
def update_status(book_id, status):
    book = Book.query.get_or_404(book_id)
    if status == 'Reserved':
        book.reader_id = current_user.id
    if status == 'Borrowed':
        book.due_date = datetime.date.today() + datetime.timedelta(days=14)
    if status == 'Available':
        book.reader_id = None
        book.due_date = None
    book.status = status
    db.session.commit()
    return redirect(request.referrer)



@api_bp.route('/create_book', methods=['POST'])
@login_required
def create_book_post():
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
                owner_id=current_user.id
                )
    return redirect(url_for('client_bp.books'))


@api_bp.route('/login', methods=['POST'])
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
    return redirect(url_for('client_bp.index'))


@api_bp.route('/signup', methods=['POST'])
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
    return redirect(url_for('client_bp.login'))


@api_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('client_bp.index'))
