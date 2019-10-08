import json
import os

from models import Author
from models import Book
from models import BookInstance

from peewee import IntegrityError


def create_author(author):
    try:
        Author.create(
            name=author.get("name", "")
        )

    except IntegrityError as e:
        print('Failed to create author.', e)


def create_book(book):
    author = Author.get(Author.name == book.get("author", ""))
    try:
        Book.create(
            title=book.get("title", ""),
            author=author.id
        )

    except IntegrityError as e:
        print('Failed to create author.', e)


def create_book_instance(book_instance):
    book = Book.get(Book.title == book_instance.get("title", ""))
    try:
        BookInstance.create(
            book=book.id,
            library_location=book_instance.get("library_location", "")
        )

    except IntegrityError as e:
        print('Failed to create author.', e)


authors_json = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'authors.json'
)
books_json = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'books.json'
)


with open(authors_json) as authors:
    try:
        authors_data = json.load(authors)
        for author in authors_data:
            create_author(author)
        print('Authors populated in database.')
    except OSError as oserr:
        print('Problem creating Authors: {}'.format(oserr))

with open(books_json) as books:
    try:
        books_data = json.load(books)
        for book in books_data:
            create_book(book)
        print('Books populated in database.')
    except OSError as oserr:
        print('Problem creating Books: {}'.format(oserr))
