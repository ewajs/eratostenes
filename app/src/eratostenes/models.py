from eratostenes import db


class Author(db.Model):
    __tablename__ = 'Author'

    AuthorID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255), nullable=False)
    BirthDate = db.Column(db.String(255))
    Bio = db.Column(db.Text)
    PicturePath = db.Column(db.String(255))
    Notes = db.Column(db.Text)
    CountryID = db.Column(db.Integer)
    UserID = db.Column(db.Integer, nullable=False)

    Book = db.relationship('Book', secondary='BookAuthor')

    def Books(self):
        return len(self.Book)

    @property
    def FullName(self):
        return self.FirstName + ' ' + self.LastName


# class BookAuthor(db.Model):
#     __tablename__ = 'BookAuthor'

#     BookID = db.Column(db.Integer, primary_key=True, nullable=False)
#     AuthorID = db.Column(db.Integer, primary_key=True,
#                          nullable=False, index=True)

t_BookAuthor = db.Table(
    'BookAuthor', db.metadata,
    db.Column('AuthorID', db.ForeignKey('Author.AuthorID'),
              primary_key=True, nullable=False),
    db.Column('BookID', db.ForeignKey('Book.BookID'),
              primary_key=True, nullable=False, index=True),
    db.Index('AuthorID', 'AuthorID', 'BookID', unique=True)
)


class Country(db.Model):
    __tablename__ = 'Country'

    CountryID = db.Column(db.Integer, primary_key=True)
    CountryName = db.Column(db.String(255), nullable=False)


class Genre(db.Model):
    __tablename__ = 'Genre'

    GenreID = db.Column(db.Integer, primary_key=True)
    GenreName = db.Column(db.String(255), nullable=False)


class User(db.Model):
    __tablename__ = 'User'

    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255), nullable=False, unique=True)
    Hash = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=True)

    def to_dict(self):
        return {'UserID': self.UserID,
                'Username': self.Username}


class Book(db.Model):
    __tablename__ = 'Book'

    BookID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    Subtitle = db.Column(db.String(511), nullable=False)
    Pages = db.Column(db.Integer)
    PublicationDate = db.Column(db.String(255))
    ISBN = db.Column(db.String(255))
    Blurb = db.Column(db.Text)
    Notes = db.Column(db.Text)
    CoverPath = db.Column(db.String(255))
    UserID = db.Column(db.ForeignKey('User.UserID'), db.ForeignKey(
        'User.UserID'), nullable=False, index=True)

    User = db.relationship('User', primaryjoin='Book.UserID == User.UserID')
    User1 = db.relationship('User', primaryjoin='Book.UserID == User.UserID')
    Quote = db.relationship('Quote', primaryjoin='Book.BookID == Quote.BookID')
    Genre = db.relationship('Genre', secondary='BookGenre')
    Author = db.relationship('Author', secondary='BookAuthor')

    def Quotes(self):
        return len(self.Quote)

    def Authors(self):
        return len(self.Author)

    def to_dict(self):
        return {'BookID': self.BookID,
                'Title': self.Title,
                'Subtitle': self.Subtitle,
                'Pages': self.Pages,
                'PublicationDate': self.PublicationDate,
                'ISBN': self.ISBN,
                'Blurb': self.Blurb,
                'Notes': self.Notes,
                'CoverPath': self.CoverPath,
                'UserID': self.UserID}


class Tag(db.Model):
    __tablename__ = 'Tag'
    __table_args__ = (
        db.Index('Tagdb.Text', 'TagText', 'UserID', unique=True),
    )

    TagID = db.Column(db.Integer, primary_key=True)
    TagText = db.Column(db.String(255), nullable=False)
    UserID = db.Column(db.ForeignKey('User.UserID'),
                       nullable=False, index=True)

    User = db.relationship('User')


t_BookGenre = db.Table(
    'BookGenre', db.metadata,
    db.Column('BookID', db.ForeignKey('Book.BookID'),
              primary_key=True, nullable=False),
    db.Column('GenreID', db.ForeignKey('Genre.GenreID'),
              primary_key=True, nullable=False, index=True),
    db.Index('BookID', 'BookID', 'GenreID', unique=True)
)


class Quote(db.Model):
    __tablename__ = 'Quote'

    QuoteID = db.Column(db.Integer, primary_key=True)
    BookID = db.Column(db.ForeignKey('Book.BookID'),
                       nullable=False, index=True)
    UserID = db.Column(db.ForeignKey('User.UserID'),
                       nullable=False, index=True)
    Page = db.Column(db.Integer)
    CharacterName = db.Column(db.String(255))
    QuoteText = db.Column(db.Text, nullable=False)
    Notes = db.Column(db.Text)

    Book = db.relationship('Book')
    User = db.relationship('User')
    Tag = db.relationship('Tag', secondary='QuoteTag')


t_QuoteTag = db.Table(
    'QuoteTag', db.metadata,
    db.Column('QuoteID', db.ForeignKey('Quote.QuoteID'), nullable=False),
    db.Column('TagID', db.ForeignKey('Tag.TagID'), nullable=False, index=True),
    db.Index('QuoteID', 'QuoteID', 'TagID', unique=True)
)
