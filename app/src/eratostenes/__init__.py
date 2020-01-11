from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


#######################################################################
# Jinja2 Template Helper Function
#######################################################################

def make_author_list(author):
    """Produces a string of author or authors"""

    names_list = [a.FirstName + ' ' + a.LastName for a in author]
    if len(names_list) == 1:
        return names_list[0]
    else:
        return ', '.join(names_list[:-1]) + ' y ' + names_list[-1]

#######################################################################
# Initialization
#######################################################################


app = Flask(__name__)
app.config.from_object(Config)
app.add_template_global(make_author_list, name='make_author_list')
db = SQLAlchemy(app)

from eratostenes import models
from eratostenes import routes
