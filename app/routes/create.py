from flask import Flask, render_template, request, redirect, Blueprint
from database.db import db
from app.services.models import Recipe


create_bp = Blueprint("create", __name__)

# Routes to /create where user can create a recipe
@create_bp.route('/create',methods = ['POST','GET'])
def create():
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
        return render_template('addrecipe.html')
      