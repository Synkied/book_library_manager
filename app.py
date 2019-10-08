from flask import abort
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask import request
from flask.views import MethodView
import jwt
from peewee import IntegrityError

from exceptions import UniqueConstraint
from models import Author
from models import Book
from models import BookInstance
from models import User

from werkzeug.exceptions import HTTPException

app = Flask(__name__)
CORS(app)
debug = True


@app.errorhandler(UniqueConstraint)
def handle_unique_constraint(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(Exception)
def handle_error(error):
    code = 400
    if isinstance(error, HTTPException):
        code = error.code
    return jsonify(error=str(error)), code


@app.route('/')
def home():
    return jsonify({'Hello': 'World'})


class UserRegisterView(MethodView):
    def post(self):
        try:
            post_data = request.get_json()
            user = User.create(**post_data)
            query = User.select().where(
                User.username == user.username,
                User.email == user.email,
            )
            serialized_data = [q.serialize for q in query]
            response = jsonify({'data': serialized_data})
            response.status_code = 201
            return response
        except Exception:
            abort(400)


class UserDeleteView(MethodView):
    def post(self):
        try:
            post_data = request.get_json()
            query = User.delete().where(
                User.username == post_data['username']
            )
            query.execute()
            message = 'User: {} deleted.'.format(post_data['username'])
            response = jsonify({'data': message})
            response.status_code = 200
            return response
        except Exception:
            abort(400)


class BookView(MethodView):
    def get(self):
        books = Book.select()
        data = [book.serialize for book in books]
        if data:
            response = jsonify({
                "count": len(data),
                "books": data,
            })
            response.status_code = 200
        else:
            output = {
                "error": "No results found."
            }
            response = jsonify(output)
            response.status_code = 404
        return response

    def post(self):
        try:
            post_data = request.get_json()
            book = Book.create(**post_data)
            query = Book.select().where(
                Book.title == book.title,
                Book.author == book.author,
            )
            serialized_data = [q.serialize for q in query]
            response = jsonify({'data': serialized_data})
            response.status_code = 201
            return response
        except IntegrityError:
            raise UniqueConstraint(
                'This book already exists.',
                status_code=400
            )


class BookDeleteView(MethodView):
    def post(self):
        try:
            post_data = request.get_json()
            print(post_data)
            query = Book.delete().where(
                Book.title == post_data['title'],
                Book.author == post_data['author'],
            )
            query.execute()
            message = 'Book: {}, {} deleted.'.format(
                post_data['title'], post_data['author']
            )
            response = jsonify({'data': message})
            response.status_code = 200
            return response
        except Exception:
            abort(400)


class AuthorView(MethodView):
    def get(self):
        authors = Author.select()
        data = [author.serialize for author in authors]
        if data:
            response = jsonify({
                "count": len(data),
                "authors": data,
            })
            response.status_code = 200
        else:
            output = {
                "error": "No results found."
            }
            response = jsonify(output)
            response.status_code = 404
        return response

    def post(self):
        try:
            post_data = request.get_json()
            author = Author.create(**post_data)
            query = Author.select().where(
                Author.name == author.name,
            )
            serialized_data = [q.serialize for q in query]
            response = jsonify({'data': serialized_data})
            response.status_code = 201
            return response
        except IntegrityError:
            raise UniqueConstraint(
                'This author already exists.',
                status_code=400
            )


class AuthorDeleteView(MethodView):
    def post(self):
        try:
            post_data = request.get_json()
            query = Author.delete().where(Author.name == post_data['name'])
            query.execute()
            message = 'Author: {} deleted.'.format(post_data['name'])
            response = jsonify({'data': message})
            response.status_code = 200
            return response
        except Exception:
            abort(400)


app.add_url_rule('/api/book', view_func=BookView.as_view('BookView'))
app.add_url_rule('/api/book/delete',
                 view_func=BookDeleteView.as_view('BookDeleteView'))
app.add_url_rule('/api/author', view_func=AuthorView.as_view('AuthorView'))
app.add_url_rule('/api/author/delete',
                 view_func=AuthorDeleteView.as_view('AuthorDeleteView'))
app.add_url_rule('/user/register',
                 view_func=UserRegisterView.as_view('UserRegisterView'))
app.add_url_rule('/user/delete',
                 view_func=UserDeleteView.as_view('UserDeleteView'))

if __name__ == '__main__':
    app.run(debug=debug)
