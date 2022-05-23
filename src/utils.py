import datetime

import pickle
from flask_wtf import FlaskForm
from sqlalchemy import or_, func
from wtforms import StringField, SelectField, IntegerField

from src import db
from src.models import Book


class BookSearchForm(FlaskForm):
    search = StringField('')


class BookAddForm(FlaskForm):
    with open('src/data/genres.pickle', 'rb') as handle:
        choices = pickle.load(handle)
    title = StringField('title')
    author = StringField('author')
    # set default genre if database is empty
    genre = SelectField(u'genre', choices=choices)
    year = IntegerField('year')


def book_search(search_str, initial_query):
    search_str = search_str.lower()
    result = initial_query.filter(
        or_(func.lower(Book.title).contains(search_str),
            func.lower(Book.genre).contains(search_str),
            func.lower(Book.author).contains(search_str)
            )).order_by(Book.title.asc())
    return result


def query_to_dict(book_query):
    book_dict = [{'title': book.title,
                  'author': book.author,
                  'genre': book.genre,
                  'year': book.year,
                  'status': book.status,
                  'id': book.id,
                  'due_date': book.due_date.strftime("%m/%d/%Y") if book.due_date else '',
                  'overdue': False if not book.due_date or datetime.date.today() < book.due_date else True
                  } for book in book_query.all()]
    return book_dict
