from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import Model
from peewee import SqliteDatabase
from config import DATABASE
from werkzeug.security import generate_password_hash, check_password_hash

library_db = SqliteDatabase(DATABASE)


class Author(Model):
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


class Book(Model):
    title = CharField()
    author = ForeignKeyField(Author)

    @property
    def serialize(self):
        serialized_data = {
            'id': self.id,
            'title': str(self.title).strip(),
            'author_name': self.author.name,
        }
        return serialized_data

    def __str__(self):
        return '{0} ({1}, {2})'.format(self.id, self.title, self.author)

    class Meta:
        indexes = (
            (('title', 'author'), True),
        )
        database = library_db


class BookInstance(Model):
    book = ForeignKeyField(Book)
    library_location = CharField()

    @property
    def serialize(self):
        serialized_data = {
            'id': self.id,
            'book': self.book,
            'library_location': str(self.library_location).strip(),
        }
        return serialized_data

    def __str__(self):
        return '{0} ({1}), {2}'.format(
            self.id, self.book.title, self.library_location
        )

    class Meta:
        indexes = (
            (('library_location',), True),
        )
        database = library_db


class User(Model):
    """An admin user capable of viewing reports.
    :param str email: email address of user
    :param str password: encrypted password for the user
    """
    username = CharField()
    email = CharField()
    password = CharField()
    created_on = DateTimeField()

    def __init__(self, username, email, password):
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

    def to_dict(self):
        return dict(id=self.id, email=self.email)

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
                Book,
                BookInstance,
                User,
            ]
        )


if __name__ == "__main__":
    create_tables()
