from flask_login import UserMixin

from src import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    author = db.Column(db.String(256))
    genre = db.Column(db.String(256))
    year = db.Column(db.Integer)
    status = db.Column(db.String(256))
    due_date = db.Column(db.Date)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reader_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, author, genre, year, owner_id, reader_id, status):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.owner_id = owner_id
        self.reader_id = reader_id
        self.status = status

    @staticmethod
    def create(title, author, genre, year, owner_id, reader_id=None, status='Available'):  # create new book
        new_book = Book(title, author, genre, year, owner_id, reader_id, status)
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
