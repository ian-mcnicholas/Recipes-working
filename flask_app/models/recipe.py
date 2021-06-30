from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models.user import User


class Recipe:
    def __init__(self, data):
      self.id = data['id']
      self.name = data['name']
      self.description = data['description']
      self.under_30 = data['under_30']
      self.instructions = data['instructions']
      self.date_made = data['date_made']
      self.created_at = data['created_at']
      self.updated_at = data['updated_at']
      self.creator = None

    @staticmethod
    def validate_recipe(data):
      is_valid = True

      if len(data['name']) < 2:
          flash("Recipe name must be at least 3 characters.")
          is_valid = False
      if (data['date_made']) == '':
          flash("Please select the date recipe was made.")
          is_valid = False
      if len(data['description']) < 3:
          flash("Description must be atleast 3 characters.")
          is_valid = False
      if len(data['instructions']) < 3:
          flash("Instructions must be atleast 3 characters.")
          is_valid = False

      return is_valid

    @classmethod
    def create_recipe(cls, data):
        query = 'INSERT INTO recipes (name, description, under_30, instructions, date_made, creator_id) VALUES (%(name)s, %(description)s, %(under_30)s, %(instructions)s, %(date_made)s, %(creator_id)s)'

        data = {
            'name': data['name'],
            'description': data['description'],
            'under_30': data['under_30'],
            'instructions': data['instructions'],
            'date_made': data['date_made'],
            'creator_id': data['creator_id'],
        }

        connection = connectToMySQL('recipes')
        results = connection.query_db(query, data)
        return results

    @classmethod
    def get_recipes(cls):
      query = 'SELECT * FROM recipes JOIN users ON users.id = recipes.creator_id'
      connection = connectToMySQL('recipes')
      results = connection.query_db(query)

      recipes = []

      for result in results:
          recipe = cls(result)
          user_data = {
              'id': result['users.id'],
              'first_name': result['first_name'],
              'last_name': result['last_name'],
              'email': result['email'],
              'password': result['password'],
              'created_at': result['users.created_at'],
              'updated_at': result['users.updated_at']
          }
          recipe.creator = User(user_data)
          recipes.append(recipe)
      return recipes

    @classmethod
    def get_recipe_by_id(cls, data):
      query = 'SELECT * FROM recipes JOIN users ON users.id = recipes.creator_id WHERE recipes.id = %(id)s'

      connection = connectToMySQL('recipes')
      results = connection.query_db(query, data)

      if len(results) == 0:
        flash('No recipe with that ID')
        return False

      else:
        result = results[0]
        recipe = cls(result)
        user_data = {
            'id': result['users.id'],
            'first_name': result['first_name'],
            'last_name': result['last_name'],
            'email': result['email'],
            'password': result['password'],
            'created_at': result['users.created_at'],
            'updated_at': result['users.updated_at']
        }
        recipe.creator = User(user_data)
        return recipe

    @classmethod
    def update_recipe(cls, data):
        query = 'UPDATE recipes SET name=%(name)s, description=%(description)s, under_30=%(under_30)s,instructions=%(instructions)s, date_made=%(date_made)s WHERE id = %(recipe_id)s;'

        connection = connectToMySQL('recipes')
        connection.query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s'

        connection = connectToMySQL('recipes')
        connection.query_db(query, data)
