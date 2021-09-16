from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.models.like import Like
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    print(pw_hash)

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }

    user_id = User.create_user(data)

    session['user_id'] = user_id

    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        flash("You must be logged in to view that page.", 'authorization')
        return redirect('/')

    data = {
        "user_id": session["user_id"]
    }

    user = User.show_user(data)
    recipes = Recipe.show_recipes()

    # make sure that the user doesn't like a recipe twice
    for recipe in recipes:
        recipe.is_unliked = Like.can_like(session["user_id"], recipe.id)

    return render_template('dashboard.html', user=user, recipes=recipes)


@app.route('/login', methods=['POST'])
def login():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", 'login')
        return redirect('/')

    session['user_id'] = user_in_db.id

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

