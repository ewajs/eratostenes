from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField, SelectMultipleField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional, Email, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from eratostenes.models import Country, Genre
from eratostenes import app


def possible_countries():
    return Country.query

def possible_genres():
    return Genre.query

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, message=('Your username is too short, 4 chars minimum.'))])
    email = StringField('Email address', [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=7, message=('Your password is too short. 7 chars minimum.'))])
    password_verify = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class AuthorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    birthdate = DateField('Birthday', format='%Y-%m-%d', validators=[Optional()])
    country = QuerySelectField(
        'Country', query_factory=possible_countries, get_label='CountryName', allow_blank=False)
    bio = TextAreaField('Bio')
    notes = TextAreaField('Notes')
    picture = FileField('Picture', validators=[
                        FileAllowed(app.config['ALLOWED_EXTENSIONS'], 'Image format not supported, allowed extensions are ' + ', '.join(app.config['ALLOWED_EXTENSIONS']))])
    keep_adding = BooleanField('Continue adding authors')
    submit = SubmitField('Submit')


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle')
    pages = IntegerField('Pages', validators=[DataRequired()])
    publication_date = DateField('Publication Date', format='%Y-%m-%d', validators=[Optional()])
    authors = QuerySelectMultipleField('Author(s)', get_label='FullName', allow_blank=False)
    genres = QuerySelectMultipleField('Genre(s)', query_factory=possible_genres, get_label='GenreName', allow_blank=False)
    isbn = StringField('ISBN')
    blurb = TextAreaField('Blurb')
    notes = TextAreaField('Notes')
    picture = FileField('Cover', validators=[
                        FileAllowed(app.config['ALLOWED_EXTENSIONS'], 'Image format not supported, allowed extensions are ' + ', '.join(app.config['ALLOWED_EXTENSIONS']))])
    keep_adding = BooleanField('Continue adding books for the same Author(s)')
    submit = SubmitField('Submit')

class QuoteForm(FlaskForm):
    page = IntegerField('Pages', validators=[DataRequired()])
    book = SelectField('Book', validators=[DataRequired()])
    character = StringField('ISBN')
    quote = TextAreaField('Blurb', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    
    submit = SubmitField('Submit')