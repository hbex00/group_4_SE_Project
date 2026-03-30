from flask import Flask, render_template, request, redirect, Blueprint
from database.db import db
from app.services.models import Recipe

#this creates a new blueprint to use
home_bp = Blueprint("home", __name__)

@home_bp.route('/',methods = ['POST','GET'])
def home():
    if request.method == 'POST':
        recipe_name = request.form['title']
        new_recipe = Recipe(recipe_title = recipe_name)

        try:
            db.session.add(new_recipe)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an error'

    else:
        recipe = Recipe.query.all()
        return render_template('addrecipe.html', recipies = recipe)
        