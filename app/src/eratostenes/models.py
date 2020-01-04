from eratostenes import db

db.Model.metadata.reflect(db.engine)
User = db.metadata.tables['User']
Author = db.metadata.tables['Author']
BookAuthor = db.metadata.tables['BookAuthor']
BookGenre = db.metadata.tables['BookGenre']
Quote = db.metadata.tables['Quote']
