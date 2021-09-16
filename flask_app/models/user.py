from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @staticmethod
    def validate_user(user):
        # user is referring to the user form
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", 'register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", 'register')
            is_valid = False
        if not user['first_name'].isalpha():
            flash("First name must only contain letters.", 'register')
            is_valid = False
        if not user['last_name'].isalpha():
            flash("Last name must only contain letters.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.", 'register')
            is_valid = False

        # query the database to find a similar email address
        data = {
            'email': user['email']
        }
        query = "SELECT email FROM users WHERE email=%(email)s;"
        results = connectToMySQL('recipes_schema').query_db(query, data)

        if len(results) > 0:
            flash("Email is already in use.", 'register')
            is_valid = False

        if user['confirm_password'] != user['password']:
            flash("Passwords must match.", 'register')
            is_valid = False

        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        if(len(result) < 1):
            return False

        return cls(result[0])

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('recipes_schema').query_db(query, data)
    
    @classmethod
    def show_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        return cls(results[0])
