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
            # to be able to add ingredents we split up the list that we get from front end 
            for recipe_ingredients, recipe_amounts, recipe_units in zip(recipe_ingredients, recipe_amounts, recipe_units):
                if recipe_ingredients.strip() != "":
                    new_ingredient = Ingredient(name = recipe_ingredients, 
                                                amount = recipe_amounts, 
                                                unit = recipe_units, 
                                                recipe_id=new_recipe.id)
                    
                    db.session.add(new_ingredient)

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
      