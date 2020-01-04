from flask import jsonify, render_template, redirect
from eratostenes.forms import LoginForm
from eratostenes import app
from eratostenes import db
from eratostenes.models import User, Book, Author, Quote


@app.route('/')
def index():
    return render_template("index.html", title="Home", user="Eze")


@app.route('/user')
def user():
    users = User.query.get(5)
    return users.Username


@app.route('/author')
def author():
    return jsonify(Author.query.all())


@app.route('/quote')
def quote():
    return jsonify(Quote.query.all())


@app.route('/book')
def book():
    books = []
    for book in Book.query.all():
        books.append(book.to_dict())
    return jsonify(books)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/')
    return render_template('login.html', title="Login", form=form)
