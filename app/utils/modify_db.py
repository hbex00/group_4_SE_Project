from flask import Flask, session
from database.db import db
from app.services.models import *

def ingredients_add(ingredients, recipe_id):
    try:          
        # Ingredients is a tuple that contains lists with 3 elements (ingredient name, amount, and unit)
        for name, amount, unit in ingredients:
            added_ingredient = ingredient_create(name, amount, unit, recipe_id)
            
            if added_ingredient is not None:
                db.session.add(added_ingredient)

        db.session.commit()
    except:
        return 'there was an error adding a ingredient'
    

def ingredient_create(name, amount, unit, recipe_id):
    try:
        amo = float(eval(amount))
    except:
        return None

    if name.strip() != "" and amo > 0:
        new_ingredient = Ingredient(name = name, 
                                    amount = amo, 
                                    unit = unit, 
                                    recipe_id=recipe_id)
        return new_ingredient
    else:
        return None


def steps_add(steps , recipe_id):
    try:
        # Creates a new step for each step sent from frontend and adds it to the database
        for recipe_step in steps:
            if recipe_step.strip() != "":
                new_step = Step(name=recipe_step,
                                recipe_id=recipe_id) 
                db.session.add(new_step)
        
        db.session.commit()
    except:
        return 'there was an error adding a step'
