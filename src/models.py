from flask_login import UserMixin

from src import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    author = db.Column(db.String(256))
    genre = db.Column(db.String(256))
    year = db.Column(db.Integer)
    reserved = db.Column(db.Boolean)
    borrowed = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, author, genre, year, reserved, borrowed, user_id):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.reserved = reserved
        self.borrowed = borrowed
        self.user_id = user_id

    @staticmethod
    def create(title, author, genre, year, user_id, reserved=False, borrowed=False):  # create new book
        new_book = Book(title, author, genre, year, reserved, borrowed, user_id)
        db.session.add(new_book)
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256))
    password = db.Column(db.String(256))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    @staticmethod
    def create(name, email, password):  # create new broker
        new_user = User(name, email, password)
        db.session.add(new_user)
        db.session.commit()



class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_begin = db.Column(db.Date)
    date_end = db.Column(db.Date)
    active = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))


    def __init__(self, date_begin, date_end, active, user_id, book_id):
        self.date_begin = date_begin
        self.date_end = date_end
        self.user_id = user_id
        self.book_id = book_id
        self.active = active

    @staticmethod
    def create(date_begin, date_end, user_id, book_id, active=True):  # create new broker
        new_borrow = Borrow(date_begin, date_end, active, user_id, book_id)
        db.session.add(new_borrow)
        db.session.commit()
