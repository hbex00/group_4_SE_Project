from flask import Flask, render_template, request, redirect, Blueprint, session
from database.db import db
from app.services.models import *
from app.utils.modify_db import *


create_bp = Blueprint("create", __name__)

# Routes to /create where user can create a recipe
@create_bp.route('/create',methods = ['POST','GET'])
def create():

    # Takes the user to login-page if they are not logged in.
    if session.get('username') is None:
        return redirect('/login')


    if request.method == 'POST':
        recipe_name = request.form['title']
        recipe_description = request.form['description']

        recipe_ingredients = request.form.getlist('ingredients[]')
        recipe_amounts = request.form.getlist('amount[]')
        recipe_units = request.form.getlist('name[]')

        recipe_steps = request.form.getlist('step[]')

        username = session.get('username')
        recipe_creator = User.query.filter_by(name=username).first()

        
        try:
            #function that creats a new recipe
            new_recipe = create_recepie(recipe_name, recipe_description, recipe_creator.id)
            db.session.add(new_recipe)
            db.session.commit()
        except:
            return 'there was an error adding the recipe'
        
        #Zips three lists that are ingredients, amounts, and units
        ingredients = zip(recipe_ingredients, recipe_amounts, recipe_units)

        #Calls ingredients_add with the tuple from zip
        ingredients_add(ingredients, new_recipe.id)

        steps_add(recipe_steps, new_recipe.id )

        return redirect('/')
    else:
        return render_template('addrecipe.html')
      



def create_recepie(name, description, user_id):
        recipe = Recipe(
            recipe_title=name,
            description=description,
            user_id=user_id)

        return recipe