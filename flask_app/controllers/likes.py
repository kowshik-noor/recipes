from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.models.recipe import Recipe
from flask_app.models.like import Like

@app.route('/recipes/<int:id>/likes')
def show_likes(id):
    if not 'user_id' in session:
        flash("You must be logged in to view that page.", 'authorization')
        return redirect('/')

    data = {
        'recipe_id' : id
    }

    recipe = Recipe.show_recipe(data)

    return render_template('likes.html', recipe=recipe)


@app.route('/recipe/like/<int:id>', methods=['POST'])
def like_recipe(id):
    data = {
        'user_id' : session['user_id'],
        'recipe_id' : id
    }

    Like.like_recipe(data)

    return redirect(f"/recipes/{id}/likes")
