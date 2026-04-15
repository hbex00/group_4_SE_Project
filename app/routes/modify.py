from flask import Flask, render_template, request, redirect, Blueprint
from database.db import db
from app.services.models import *
from app.utils.modify_db import *

modify_bp = Blueprint("modify", __name__)

@modify_bp.route('/modify', methods=['POST', 'GET'])
def modify():
    recipe_id = request.args.get('recipe_id', type = int)
    recipe = Recipe.query.get_or_404(recipe_id)
    # when geting input from user we change all the inputs for a recipe in the databas  
    if request.method == 'POST' :
        recipe.recipe_title = request.form.get('title') 
        recipe.description = request.form.get('description')
        recipe.portions = request.form.get('portions')
    # we delete all the lists of ingredents and steps 
        Ingredient.query.filter_by(recipe_id = recipe_id).delete()
        Step.query.filter_by(recipe_id = recipe_id).delete()
        db.session.commit()

        ingredients = zip(
            request.form.getlist('ingredients[]'),
            request.form.getlist('amount[]'),
            request.form.getlist('unit[]')
            )

        steps = request.form.getlist("step[]")

    # then uses the functions to add them back in 
        ingredients_add(ingredients, recipe_id)
        steps_add(steps, recipe_id)

        return redirect('/viewrecipe')
        
    return render_template('modify.html', recipe=recipe)