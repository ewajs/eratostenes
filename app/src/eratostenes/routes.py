from flask import render_template, redirect, flash
from eratostenes.forms import LoginForm
from eratostenes import app
from eratostenes import db
from eratostenes.models import User, Author, Quote


@app.route('/')
def index():
    return render_template("index.html", title="Home", user="Eze")


@app.route('/user')
def user():
    return repr(User)


@app.route('/author')
def author():
    return repr(Author)


@app.route('/quote')
def quote():
    return repr(Quote)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/')
    return render_template('login.html', title="Login", form=form)
