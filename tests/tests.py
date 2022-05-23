from flask import session
from werkzeug.security import generate_password_hash

from src import db
from src.models import User, Book


def test_create_user(app):
    with app.app_context():
        User.create('name', 'email', 'password')
        assert db.session.query(User).one()


def test_delete_book_not_logged_in(app, client):
    with app.app_context():
        book = Book('title', 'author', 'genre', 1997, None, None, 'Available')
        db.session.add(book)
        db.session.commit()
        response = client.get("/book/delete/" + str(book.id))
        assert 405 == response.status_code
        assert db.session.query(Book).one()


def test_delete_book_not_logged_in(app, client):
    with app.app_context():
        book = Book('title', 'author', 'genre', 1997, None, None, 'Available')
        db.session.add(book)
        db.session.commit()
        response = client.get("/book/delete/" + str(book.id))
        assert 405 == response.status_code
        assert db.session.query(Book).one()


def test_login(app, client):
    with app.app_context():
        with client:
            password = generate_password_hash('password', method='sha256')
            User.create('name', 'email@email.com', password)
            response = client.post('/login', data={'email': 'email@email.com', 'password': 'password'})
            assert session["_user_id"] == '1'
