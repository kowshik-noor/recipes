from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.models.like import Like

@app.route('/recipes/<int:id>')
def show_recipe(id):
    if not 'user_id' in session:
        flash("You must be logged in to view that page.", 'authorization')
        return redirect('/')
    data= {
        'recipe_id' : id,
        "user_id": session["user_id"]
    }

    recipe = Recipe.show_recipe(data)
    user = User.show_user(data)

    recipe.is_unliked = Like.can_like(user.id, recipe.id)

    return render_template('show.html', recipe=recipe, user=user)

@app.route('/recipes/new', methods=['GET', 'POST'])
def new_recipe():
    if request.method == 'POST':
        if not Recipe.validate_recipe(request.form):
            return redirect('/recipes/new')

        data = {
            'name' : request.form['name'],
            'description' : request.form['description'],
            'instructions' : request.form['instructions'],
            'thirty_min' : request.form['thirty_min'],
            'created_at' : request.form['created_at'],
            'user_id' : session['user_id']
        }

        Recipe.create_recipe(data);

        return redirect('/dashboard')
    else:
        if not 'user_id' in session:
            flash("You must be logged in to view that page.", 'authorization')
            return redirect('/')

        return render_template('create.html')

@app.route('/recipes/edit/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    if request.method == 'POST':
        if not Recipe.validate_recipe(request.form):
            return redirect(f"/recipes/edit/{id}")
        data = {
            'recipe_id' : id,
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'thirty_min': request.form['thirty_min'],
            'created_at': request.form['created_at'],
            'user_id': session['user_id']
        }

        Recipe.update_recipe(data)

        return redirect('/dashboard')

    else:
        if not 'user_id' in session:
            flash("You must be logged in to view that page.", 'authorization')
            return redirect('/')

        data = {
            'recipe_id': id
        }

        recipe = Recipe.show_recipe(data)

        return render_template('/edit.html', recipe = recipe)

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    data = {
        'recipe_id': id
    }

    Recipe.delete_recipe(data)

    return redirect('/dashboard')

