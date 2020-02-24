import crypt
from eratostenes.forms import LoginForm, AuthorForm
from eratostenes import app
from eratostenes import db
from eratostenes.models import User, Book, Author, Quote, Country
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


def elapsed_time(f):
    """For testing purposes"""
    @wraps(f)
    def decorated_function(*args, **kws):
        import time
        start_time = time.time()
        rtn = f(*args, **kws)
        elapsed = time.time() - start_time
        app.logger.info("Elapsed: " + str(elapsed))
        return rtn
    return decorated_function

#######################################################################
# Functions
#######################################################################


def get_user_stats(user_id):
    authors = Author.query.with_entities(
        Author.AuthorID.distinct()).filter(Author.UserID == user_id).count()
    books = Book.query.with_entities(Book.BookID.distinct()).filter(
        Book.UserID == user_id).count()
    quotes = Quote.query.with_entities(Quote.QuoteID.distinct()).filter(
        Quote.UserID == user_id).count()
    return {'Authors': authors, 'Books': books, 'Quotes': quotes}


def get_random_quote(user_id):
    data = Quote.query.filter(Quote.UserID == user_id).order_by(
        func.rand()).limit(1).one()
    return data

def get_3by3_matrix(entity, user_id):
    data = entity.query.filter(entity.UserID == user_id).order_by(
        func.rand()).limit(9).all()
    matrix = [list(data[i:i+3]) for i in [0, 3, 6]]
    #app.logger.info(matrix)
    return matrix
    # data = Quote.query.filter(
    #     Quote.Book == Book.query.filter(
    #         Book.Title == 'Journey to the Ants').one()).order_by(func.rand()).limit(1).one()
   # Quote.UserID == user_id).order_by(func.rand()).limit(1).one()
    


#######################################################################
# Routes
#######################################################################

#######################################################################
#    Main
#######################################################################

@app.route('/')
@requires_auth
def index():
    user_id = session['user']['UserID']
    user_data = get_user_stats(user_id)
    quote = get_random_quote(user_id)

    return render_template("index.html", title="Home", username=session['user']['Username'], user_data=user_data, quote=quote)

#######################################################################
#    User
#######################################################################


@app.route('/user')
def user_route():
    users = User.query.filter(User.Username == "ewajs").first()
    return users.Email


#######################################################################
#   Author Subroutes
#######################################################################
#######################################################################
#       Add Author
#######################################################################

@app.route('/author/add')
@requires_auth
def author_add_route():
    """Serves the add author page"""
    form = AuthorForm()
    # If a valid form is received
    if form.validate_on_submit():
        #TODO: Add author to database and upload picture
        return True
    authors_matrix = get_3by3_matrix(Author, session['user']['UserID'])
    return render_template('author_add.html', title="Add Author", form=form, authors_matrix = authors_matrix)

#######################################################################
#       List Authors
#######################################################################

@app.route('/author/list')
@requires_auth
def author_list_route():
    """Serves the author list page"""
    authors = Author.query.filter(Author.UserID == session['user']['UserID']).all()
    return render_template('author_list.html', title="My Authors", authors = authors)

#######################################################################
#       Author by ID
#######################################################################


@app.route('/author/<int:author_id>')
@requires_auth
def author_route(author_id):
    """Renders Author with AuthorID equal to author_id for the logged user"""
    author = Author.query.filter((Author.AuthorID == author_id) & (
        Author.UserID == session['user']['UserID'])).one()
    return render_template('author.html', title=author.FullName, authors=[author, ])


#######################################################################
#       Book(s) of Author by ID
#######################################################################

@app.route('/author/<int:author_id>/books')
@requires_auth
def author_book_route(author_id):
    """Renders Books of Author with AuthorID equal to author_id for the logged user"""
    author = Author.query.filter((Author.AuthorID == author_id) & (
        Author.UserID == session['user']['UserID'])).one()
    books = author.Book
    title = "Books of " + author.FullName
    return render_template('book.html', title=title, author=author, books=books)


#######################################################################
#   Book Subroutes
#######################################################################

@app.route('/author/add')
@requires_auth
def book_add_route():
    """Serves the add book page"""
    form = BookForm()
    # TODO: Continue working here
    form.authors.choices = [(author.AuthorID, author.FullName) for author in Author.query.filter(Author.UserID == session['user']['UserID']).all()]
    # If a valid form is received
    if form.validate_on_submit():
        #TODO: Add book to database and upload picture
        return True
    books_matrix = get_3by3_matrix(Book, session['user']['UserID'])
    return render_template('book_add.html', title="Add Book", form=form, books_matrix = books_matrix)


#######################################################################
#       List Books
#######################################################################

@app.route('/book/list')
@requires_auth
def book_list_route():
    """Serves the book list page"""
    books = Book.query.filter(Book.UserID == session['user']['UserID']).all()
    return render_template('book_list.html', title="My Books", books = books)

#######################################################################
#       Book by ID
#######################################################################

@app.route('/book/<int:book_id>')
@requires_auth
def book_route(book_id):
    """Renders Book with BookID equal to book_id for the logged user"""
    book = Book.query.filter((Book.BookID == book_id) & (
        Author.UserID == session['user']['UserID'])).one()
    app.logger.info(book.Quotes)
    return render_template('book.html', title=book.Title, books=[book, ])

#######################################################################
#       Author(s) of Book by ID
#######################################################################


@app.route('/book/<int:book_id>/authors')
@requires_auth
def book_author_route(book_id):
    """Renders Author(s) of Book with BookID equal to book_id for the logged user"""
    book = Book.query.filter((Book.BookID == book_id) & (
        Author.UserID == session['user']['UserID'])).one()
    authors = book.Author
    title = "Author of " + book.Title
    return render_template('author.html', title=title, authors=authors, book=book)


#######################################################################
#    Quote Subroutes
#######################################################################

@app.route('/quote')
def quote():
    return jsonify(Quote.query.all())


#######################################################################
#    Login
#######################################################################

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


#######################################################################
#   Logout
#######################################################################

@app.route('/logout')
def logout():
    """Logs out the user"""
    session['user'] = None
    return redirect(url_for('login'))
