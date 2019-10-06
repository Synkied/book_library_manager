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

app = Flask(__name__)
CORS(app)
debug = True


@app.errorhandler(UniqueConstraint)
def handle_unique_constraint(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def home():
    return jsonify({'Hello': 'World'})


class RegisterView(MethodView):
    def post(self):
        try:
            post_data = request.get_json()
            User.create(**post_data)
            user = User.select(
                User.username == post_data.username,
                User.email == post_data.email,
            )
            response = jsonify(user.to_dict())
            response.status_code = 201
            return response
        except Exception as err:
            print(err)
            return jsonify({'toto': 'tutu'})


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
            data = request.get_json()
            post_data = Book.create(**data)
            query = Book.select().where(
                Book.title == post_data.title,
                Book.author == post_data.author
            )
            data = [q.serialize for q in query]
            response = jsonify({'data': data})
            response.status_code = 201
            return jsonify(response)
        except IntegrityError:
            raise UniqueConstraint(
                'This book already exists.',
                status_code=400
            )


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
            data = request.get_json()
            post_data = Book.create(**data)
            query = Author.select().where(
                Author.name == post_data.name,
            )
            data = [q.serialize for q in query]
            response = jsonify({'data': data})
            response.status_code = 201
            return jsonify(response)
        except IntegrityError:
            raise UniqueConstraint(
                'This author already exists.',
                status_code=400
            )


app.add_url_rule('/api/books', view_func=BookView.as_view('BookView'))
app.add_url_rule('/api/authors', view_func=AuthorView.as_view('AuthorView'))
app.add_url_rule('/register', view_func=RegisterView.as_view('RegisterView'))

if __name__ == '__main__':
    app.run(debug=debug)
