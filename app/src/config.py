import os
from os import getenv


class Config(object):
    DB_HOST = getenv('DATABASE_HOST')
    DB_USER = getenv('MYSQL_USER')
    DB_PASS = getenv('MYSQL_PASSWORD')
    DB_NAME = getenv('MYSQL_DATABASE')
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + getenv('MYSQL_USER') + ':' + \
        getenv('MYSQL_PASSWORD') + '@' + getenv('DATABASE_HOST') + \
        '/' + getenv('MYSQL_DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    UPLOAD_FOLDER = getenv('UPLOAD_FOLDER')
    MAX_CONTENT_LENGTH = int(getenv('MAX_CONTENT_LENGTH'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


if __name__ == '__main__':
    DB_HOST = getenv('DATABASE_HOST')
    print(DB_HOST)
    DB_USER = getenv('MYSQL_USER')
    print(DB_USER)
    DB_PASS = getenv('MYSQL_PASSWORD')
    print(DB_PASS)
    DB_NAME = getenv('MYSQL_DATABASE')
    print(DB_NAME)
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = 'mysql://' + getenv('MYSQL_USER') + ':' + \
        getenv('MYSQL_PASSWORD') + '@' + getenv('DATABASE_HOST') + \
        '/' + getenv('MYSQL_DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
