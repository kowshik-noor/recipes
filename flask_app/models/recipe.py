from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.thirty_min = data['thirty_min']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # a list of user instances who liked the recipe
        self.likes = []
        # query the database to get a list of users who liked the recipe
        query = "SELECT * from likes JOIN users ON users.id = likes.user_id WHERE likes.recipe_id = " + str(self.id) + ";"
        results = connectToMySQL('recipes_schema').query_db(query)

        for liker in results:
            liker_data = {
                'id': liker['users.id'],
                'first_name': liker['first_name'],
                'last_name': liker['last_name'],
                'email': liker['email'],
                'password': liker['password'],
                'created_at': liker['created_at'],
                'updated_at': liker['updated_at']
            }
            self.likes.append(User(liker_data))

        self.num_likes = len(self.likes)
        self.is_unliked = None



    @staticmethod
    def validate_recipe(recipe):
        # recipe is referring to the recipe form
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters long.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters long.")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters long.")
            is_valid = False

        # i could also validate created at if the need arises. But there might be an input type for dates.

        return is_valid
    
    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, thirty_min, created_at, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(thirty_min)s, %(created_at)s, %(user_id)s);"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        return result

    @classmethod
    def show_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []

        for recipe in results:
                recipes.append(cls(recipe))

        return recipes

    @classmethod
    def show_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(recipe_id)s;"
        result = connectToMySQL('recipes_schema').query_db(query, data)

        return cls(result[0])

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, thirty_min=%(thirty_min)s, created_at=%(created_at)s WHERE id=%(recipe_id)s;"
        connectToMySQL('recipes_schema').query_db(query, data)
    
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM likes WHERE recipe_id=%(recipe_id)s;"
        connectToMySQL('recipes_schema').query_db(query, data)
        query2 = "DELETE FROM recipes WHERE id=%(recipe_id)s;"
        connectToMySQL('recipes_schema').query_db(query2, data)




