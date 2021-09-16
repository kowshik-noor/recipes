from flask_app.config.mysqlconnection import connectToMySQL


class Like:
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.recipe_id = data["recipe_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    @classmethod
    def like_recipe(cls, data):
        query = "INSERT INTO likes (user_id, recipe_id) VALUES (%(user_id)s, %(recipe_id)s);"
        return connectToMySQL('recipes_schema').query_db(query, data)

    # a method that can check if a given user can like a recipe returns true if they can and false if they can't
    @staticmethod
    def can_like(user_id, recipe_id):
        # query the database if there is a row where the user liked the recipe
        query = f"SELECT * FROM likes WHERE user_id = {user_id} AND recipe_id = {recipe_id};"
        results = connectToMySQL('recipes_schema').query_db(query)

        return len(results) == 0
