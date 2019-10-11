import json
import os

from models import Author
from models import BookDescriptor
from models import Book

from peewee import IntegrityError


def create_author(author):
    try:
        Author.create(
            name=author.get("name", "")
        )

    except IntegrityError as e:
        print('Failed to create author.', e)


def create_book_descriptor(book_descriptor):
    author = Author.get(Author.name == book_descriptor.get("author", ""))
    try:
        BookDescriptor.create(
            title=book_descriptor.get("title", ""),
            author=author.id
        )

    except IntegrityError as e:
        print('Failed to create author.', e)


def create_book(book):
    book = BookDescriptor.get(
        BookDescriptor.title == book.get("title", "")
    )
    try:
        Book.create(
            book=book.id,
            library_location=book.get("library_location", "")
        )

    except IntegrityError as e:
        print('Failed to create author.', e)


authors_json = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'authors.json'
)
book_descriptors_json = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'book_descriptors.json'
)


with open(authors_json) as authors:
    try:
        authors_data = json.load(authors)
        for author in authors_data:
            create_author(author)
        print('Authors populated in database.')
    except OSError as oserr:
        print('Problem creating Authors: {}'.format(oserr))

with open(book_descriptors_json) as book_descriptors:
    try:
        book_descriptors_data = json.load(book_descriptors)
        for book in book_descriptors_data:
            create_book_descriptor(book)
        print('BookDescriptors populated in database.')
    except OSError as oserr:
        print('Problem creating BookDescriptors: {}'.format(oserr))
