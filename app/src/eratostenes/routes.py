import crypt
from eratostenes.forms import LoginForm
from eratostenes import app
from eratostenes import db
from eratostenes.models import User, Book, Author, Quote
from flask import jsonify, render_template, redirect, url_for, flash
from hmac import compare_digest as compare_hash


@app.route('/')
def index():
    return render_template("index.html", title="Home", user="Eze")


@app.route('/user')
def user_route():
    users = User.query.filter(User.Username == "ewajs").first()
    return users.Email


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
    """Serves the login page and logs in the user"""
    # Initialize form
    form = LoginForm()
    # If a valid form is received
    if form.validate_on_submit():
        # Retrieve user by username or email
        user = User.query.filter(
            (User.Username == form.username.data) | (User.Email == form.username.data)).first()
        # Retrieve submitted password
        password = form.password.data
        # Compare hashes
        pw_match = compare_hash(crypt.crypt(
            password, user.Hash), user.Hash)
        if pw_match:
            return render_template("OK.html", user=user, hashed_pw=pw_match)
        else:
            flash('Username and password do not match!')
            return render_template('login.html', title="Login", form=form)
    return render_template('login.html', title="Login", form=form)
