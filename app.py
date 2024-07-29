#!/usr/bin/env python

import os

from flask import Flask
from flask import render_template

from database import db, Genre, Book

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


@app.route("/")
def all_books():
    """
    Main function - output all books into template
    """
    books = Book.query.order_by("added").limit(15)
    return render_template("all_books.html", books=books)


@app.route("/genre/<int:genre_id>")
def books_by_genre(genre_id):
    """
    Outputs all the books with the given genre_id
    """
    genre = Genre.query.get_or_404(genre_id)
    return render_template(
        "books_by_genre.html",
        genre_name=genre.name,
        books=genre.books,
    )


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        # fill DB with testing data(fixtures)

        genre1 = Genre(name="жанр1")
        db.session.add(genre1)
        genre2 = Genre(name="жанр2")
        db.session.add(genre2)
        genre3 = Genre(name="жанр3")
        db.session.add(genre3)

        book1 = Book(name="Преступление", genre=genre1)
        db.session.add(book1)
        book2 = Book(name="Книга2", genre=genre2)
        db.session.add(book2)

        db.session.commit()
    app.run()
