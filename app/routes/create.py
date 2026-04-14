from flask import Flask, render_template, request, redirect, Blueprint, session
from database.db import db
from app.services.models import *


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

        new_recipe = Recipe(recipe_title = recipe_name, 
                            description = recipe_description, 
                            user_id = recipe_creator.id)


        try:
            db.session.add(new_recipe)
            db.session.commit()


            #Zips three lists that are ingredients, amounts, and units
            ingredients = zip(recipe_ingredients, recipe_amounts, recipe_units)

            #Calls ingredient_add with the tuple from zip
            ingredient_add(ingredients, new_recipe.id)


            # Creates a new step for each step sent from frontend and adds it to the database
            for recipe_step in recipe_steps:
                if recipe_step.strip() != "":
                    new_step = Step(name=recipe_step,
                                    recipe_id=new_recipe.id)

                    db.session.add(new_step)

            db.session.commit()

            return redirect('/')
        except:
            return 'there was an error'

    else:
        return render_template('addrecipe.html')
      


def ingredient_add(ingredients, recipe_id):
    # Ingredients is a tuple that contains lists with 3 elements (ingredient name, amount, and unit)
    for ingredients, amounts, units in ingredients:
            if ingredients.strip() != "":
                new_ingredient = Ingredient(name = ingredients, 
                                            amount = amounts, 
                                            unit = units, 
                                            recipe_id=recipe_id)
                
                db.session.add(new_ingredient)
