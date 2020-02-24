from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from eratostenes.models import Country


def possible_countries():
    return Country.query

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AuthorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    birthdate = DateField('Birthday', format='%d/%m/%Y', validators=[Optional()])
    country = QuerySelectField(
        'Country', query_factory=possible_countries, get_label='CountryName', allow_blank=False)
    bio = TextAreaField('Bio')
    notes = TextAreaField('Notes')
    picture = FileField('Picture', validators=[
                        FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Sign In')


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    authors = SelectMultipleField('Author(s)',validators=[DataRequired()])
    country = QuerySelectField(
        'Country', query_factory=possible_countries, get_label='CountryName', allow_blank=False)
    bio = TextAreaField('Bio')
    notes = TextAreaField('Notes')
    picture = FileField('Picture', validators=[
                        FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Sign In')