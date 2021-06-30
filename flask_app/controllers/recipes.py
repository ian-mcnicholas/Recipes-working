from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User



@app.route('/recipes/new')
def new_recipe():
    if 'user_id' in session:
        return render_template('/recipe_form.html')
    return redirect('/')


# CREATE 
@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    print(request.form)
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    Recipe.create_recipe(request.form)
    return redirect('/dashboard')

# VIEW 
@app.route('/recipes/<int:recipe_id>')
def show_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    user_id = session['user_id']
    user = User.get_user_by_id(user_id)[0]
    recipe = Recipe.get_recipe_by_id(data)
    return render_template('/show_recipe.html', recipe = recipe, user = user)

# EDIT 
@app.route('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)

    if recipe == False:
        return redirect('/dashboard')
    if recipe.creator.id != session['user_id']:
        return redirect('/dashboard')

    return render_template('/edit_recipe.html', recipe = recipe)

# UPDATE 
@app.route('/recipes/<int:recipe_id>/update', methods=['POST'])
def update_recipe(recipe_id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/{recipe_id}/edit')

    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'under_30': request.form['under_30'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'recipe_id': recipe_id
    }

    Recipe.update_recipe(data)
    return redirect('/dashboard')

# DELETE 
@app.route('/recipes/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect('/dashboard')
