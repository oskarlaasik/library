from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField

from src import db
from src.models import Book


class BookSearchForm(FlaskForm):
    search = StringField('')

class BookAddForm(FlaskForm):
    title = StringField('title')
    author = StringField('author')
    genre = SelectField(u'genre', choices=[genre[0] for genre in db.session.query(Book.genre).distinct().all()])
    year = IntegerField('year')
