import crypt
from eratostenes.forms import LoginForm
from eratostenes import app
from eratostenes import db
from eratostenes.models import User, Book, Author, Quote
from flask import flash, jsonify, render_template, redirect, request, session, url_for
from sqlalchemy.sql import func
from functools import wraps
from hmac import compare_digest as compare_hash


#######################################################################
# Helpers
#######################################################################

#######################################################################
# Decorators
#######################################################################

def requires_auth(f):
    """Minimal implementation of authentication. Will be refactored."""
    @wraps(f)
    def decorated_function(*args, **kws):
        if session.get('user', None) is None:
            return redirect(url_for('login'))
        else:
            return f(*args, **kws)
    return decorated_function

#######################################################################
# Functions
#######################################################################


def get_user_stats(user_id):
    data = User.query.with_entities(
        User.UserID, func.count(Author.AuthorID.distinct()), func.count(Book.BookID.distinct()), func.count(Quote.QuoteID.distinct())).filter(
        User.UserID == user_id).join(
        Author, User.UserID == Author.UserID).join(
        Book, User.UserID == Book.UserID).join(
        Quote, Quote.UserID == User.UserID).group_by(User.UserID).first()
    return {'Authors': data[1], 'Books': data[2], 'Quotes': data[3]}


def get_random_quote(user_id):
    data = Quote.query.filter(
        User.UserID == user_id).order_by(func.rand()).first()
    return data

#######################################################################
# Routes
#######################################################################


@app.route('/')
@requires_auth
def index():
    user_id = session['user']['UserID']
    user_data = get_user_stats(user_id)
    quote = get_random_quote(user_id)
    return render_template("index.html", title="Home", username=session['user']['Username'], user_data=user_data, quote=quote)


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
    if session.get('user', None) is not None:  # Redirect already atuhenticated users to home
        return redirect('/')
    # Initialize form
    form = LoginForm()
    # If a valid form is received
    if form.validate_on_submit():
        # Retrieve user by username or email
        user = User.query.filter(
            (User.Username == form.username.data) | (User.Email == form.username.data)).first()
        if user:  # Found user
            # Retrieve submitted password
            password = form.password.data
            # Compare hashes
            pw_match = compare_hash(crypt.crypt(
                password, user.Hash), user.Hash)
            if pw_match:
                session['user'] = user.to_dict()
                return redirect(url_for('index'))
            else:  # No user or email found
                flash('Unrecognized username and/or password!')
                return render_template('login.html', title="Login", form=form)
        else:
            flash('Unrecognized username and/or password!')
            return render_template('login.html', title="Login", form=form)
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
def logout():
    """Logs out the user"""
    session['user'] = None
    return redirect(url_for('login'))
