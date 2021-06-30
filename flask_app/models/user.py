from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_regex = re.compile(r'^(?=.*\d)(?=.*[A-Z])(?!.*[^a-zA-Z0-9@#$^+=])(.{8,})$')

class User:
    def __init__(self, data):
      self.id = data['id']
      self.first_name = data['first_name']
      self.last_name = data['last_name']
      self.email = data['email']
      self.password = data['password']
      self.created_at = data['created_at']
      self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(data):
      is_valid = True

      if len(data['first_name']) < 2:
          flash("Name must be at least 2 characters.")
          is_valid = False
      if len(data['last_name']) < 2:
          flash("Last name must be at least 2 characters.")
          is_valid = False
      if not email_regex.match(data['email']):
          flash("Invalid email address!")
          is_valid = False
      if  len(User.get_user_by_email(data)) != 0:
          flash("User with this email already exits")
          is_valid = False
      if not password_regex.match(data['password']):
          flash("Password must contain atleast 1 uppercase letter and number and have a minimum of 8 characters.")
          is_valid = False
      if data['password_confirm'] != data['password']:
          flash("Password inputs need to match")
          is_valid = False
      return is_valid

    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password, subscription) VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s, %(subscription)s)'
        pw_hash = bcrypt.generate_password_hash(data['password'])
        data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': pw_hash,
            'subscription': data.get('subscription')
        }
        connection = connectToMySQL('recipes')
        results = connection.query_db(query, data)
        return results

    @classmethod
    def get_user_by_email(cls, data):
      query = 'SELECT * FROM users WHERE users.email = %(email)s'
      data = {
        'email': data['email']
      }
      connection = connectToMySQL('recipes')
      results = connection.query_db(query, data)

      users = []
      for user in results:
          users.append(cls(user))

      return users

    @classmethod
    def get_user_by_id(cls, user_id):
      query = 'SELECT * FROM users WHERE users.id = %(id)s'
      data = {
        'id': user_id
      }
      results = connectToMySQL('recipes').query_db(query, data)

      users = []
      for user in results:
          users.append(cls(user))

      return users

