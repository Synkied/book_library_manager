from datetime import datetime

from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import Model
from peewee import SqliteDatabase
from config import DATABASE
from werkzeug.security import generate_password_hash, check_password_hash

library_db = SqliteDatabase(DATABASE, pragmas=[('foreign_keys', 'on')])


class Author(Model):
    """
    A book author.
    :param str name: author's name
    """
    name = CharField()

    @property
    def serialize(self):
        serialized_data = {
            'id': self.id,
            'name': str(self.name).strip(),
        }
        return serialized_data

    class Meta:
        indexes = (
            (('name',), True),
        )
        database = library_db


class BookDescriptor(Model):
    """
    A book descriptor object.
    :param str title: book's title
    :param fk author: book's author
    """
    title = CharField()
    author = ForeignKeyField(Author, on_delete='CASCADE')

    @property
    def serialize(self):
        serialized_data = {
            'id': self.id,
            'title': str(self.title).strip(),
            'author_name': self.author.name,
            'author': self.author.id,
        }
        return serialized_data

    def __str__(self):
        return '{0} ({1}, {2})'.format(self.id, self.title, self.author)

    class Meta:
        indexes = (
            (('title', 'author'), True),
        )
        database = library_db


class Book(Model):
    """
    A book instance. Because one book can be bought multiple times
    by the library
    :param fk book: the book
    :param str library_location: book instance's location in the library
    """
    book_descriptor = ForeignKeyField(BookDescriptor, on_delete='CASCADE')
    library_location = CharField()

    @property
    def serialize(self):
        serialized_data = {
            'id': self.id,
            'book_descriptor': self.book_descriptor.id,
            'library_location': str(self.library_location).strip(),
        }
        return serialized_data

    def __str__(self):
        return '{0} ({1}), {2}'.format(
            self.id, self.book_descriptor.title, self.library_location
        )

    class Meta:
        indexes = (
            (('library_location',), True),
        )
        database = library_db


class User(Model):
    """
    An admin user capable of viewing reports.
    :param str username: user's username
    :param str email: email address of user
    :param str password: encrypted password for the user
    :param datetime created_on: user's creation date in db
    """
    username = CharField()
    email = CharField()
    password = CharField()
    created_on = DateTimeField(default=datetime.now)

    def __init__(self, username, email, password, **kwargs):
        super(User, self).__init__(
            self,
            username=username,
            email=email,
            password=password,
            **kwargs
        )
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    @property
    def serialize(self):
        serialized_data = {
            'id': self.id,
            'email': self.email,
            'username': self.username,
        }
        return serialized_data

    def __repr__(self):
        return '<User {}>'.format(self.username)

    class Meta:
        indexes = (
            (('username',), True),
            (('email',), True),
        )
        database = library_db


def create_tables():
    with library_db:
        library_db.create_tables(
            [
                Author,
                BookDescriptor,
                Book,
                User,
            ]
        )


if __name__ == "__main__":
    create_tables()
