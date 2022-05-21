import csv
import datetime
import random

from sqlalchemy import func
from werkzeug.security import generate_password_hash

from src import init_app
from src.models import *


def insert_dummy_data():
    app = init_app()
    with app.app_context():
        Borrow.query.delete()
        Book.query.delete()
        User.query.delete()

        names = ['Mari', 'Peeter', 'Toomas', 'Liisa']
        users = []

        for name in names:
            email = name.lower() + '@mail.ee'
            password = '****'
            new_user = User(name, email, generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            users.append(new_user)

        with open('tests/data/Top UK book sales of all time - Top 100 199801-201231.tsv', newline='') as csvfile:
            book_reader = csv.reader(csvfile, delimiter="\t")
            # skip the headers
            next(book_reader, None)
            for book in book_reader:
                Book.create(title=book[1],
                            author=book[2],
                            year=book[7].split()[-1],
                            genre=book[8],
                            user_id=random.choice(users).id
                            )

        books = Book.query.order_by(func.random()).limit(16).all()
        date_begin = datetime.date.today()
        date_end = date_begin + datetime.timedelta(days=14)
        for book in books:
            Borrow.create(date_begin=date_begin,
                          date_end=date_end,
                          #Remove book owner from potential borrower list
                          user_id=random.choice([user for user in users if user.id != book.id]).id,
                          book_id=book.id
                          )


if __name__ == "__main__":
    insert_dummy_data()
