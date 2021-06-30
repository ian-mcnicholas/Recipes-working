from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('/login.html')

@app.route('/dashboard')
def success():
    if 'user_id' in session:
        # passing user id from session to query messages by user
        user_id = session['user_id']
        user = User.get_user_by_id(user_id)[0]
        recipes = Recipe.get_recipes()
        print(recipes)
        return render_template('/dashboard.html', user = user, recipes = recipes)
    return redirect('/')

# CREATE 
@app.route('/users/create', methods=['POST'])
def register_user():
    if not User.validate_user(request.form):
        session['reg_submit'] = True
        session['login_submit'] = False
        return redirect('/')
    new_user = User.create_user(request.form)
    # STORE SESSION DATA
    session['user_id'] = new_user
    return redirect('/dashboard')

# LOGIN 
@app.route('/login', methods=['POST'])
def login_user():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_user_by_email(data)[0]
    if not user_in_db:
        session['reg_submit'] = False
        session['login_submit'] = True
        flash("No match found")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("No match found")
        return redirect('/')
    # STORE SESSION DATA
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    session['logged_in'] = False
    return redirect('/')
