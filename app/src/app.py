from eratostenes import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

# from flask import Flask, escape, request, jsonify
# import pymysql
# import pymysql.cursors
# from os import getenv

# app = Flask(__name__)

# DB_HOST = getenv('DATABASE_HOST')
# DB_USER = getenv('MYSQL_USER')
# DB_PASS = getenv('MYSQL_PASSWORD')
# DB_NAME = getenv('MYSQL_DATABASE')

#
# @app.route('/')
# def hello():
#     #name = request.args.get("name", "World")
#     # Connect to the database
#     connection = pymysql.connect(host=DB_HOST,
#                                  user=DB_USER,
#                                  password=DB_PASS,
#                                  db=DB_NAME,
#                                  charset='utf8mb4',
#                                  cursorclass=pymysql.cursors.DictCursor)

#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM Author LIMIT 4")
#             data = cursor.fetchall()
#     finally:
#         connection.close()

#     return jsonify(data)


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80)
