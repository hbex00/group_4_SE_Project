from flask import Flask, render_template, request, redirect, Blueprint, session, current_app
from database.db import db
from app.services.models import *
from app.utils.modify_db import *
from app.utils.tag import *
from app.utils.helper_function import *
import uuid
from werkzeug.utils import secure_filename
import os


create_bp = Blueprint("create", __name__)

# Routes to /create where user can create a recipe
@create_bp.route('/create',methods = ['POST','GET'])
def create():

    # Takes the user to login-page if they are not logged in.
    if session.get('id') is None:
        return redirect('/login')


    if request.method == 'POST':
        recipe_name = request.form['title']
        file = request.files.get('file')
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_name = str(uuid.uuid4()) + "_" + filename
                UPLOAD_FOLDER = os.path.join(current_app.static_folder, "Bilder", "recipe_pics")
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, unique_name))
                recipe_image = unique_name
        else:
            recipe_image = None
        recipe_description = request.form['description']
        recipe_portions = request.form['portions']

        recipe_ingredients = request.form.getlist('ingredients[]')
        recipe_amounts = request.form.getlist('amount[]')
        recipe_units = request.form.getlist('unit[]')

        recipe_steps = request.form.getlist('step[]')

        tag_list = request.form.getlist('tag[]')

        id = session.get('id')
        recipe_creator = User.query.filter_by(id=id).first()

        
        try:
            #function that creats a new recipe
            new_recipe = create_recepie(recipe_name, recipe_description, recipe_portions, recipe_creator.id,recipe_image)
            db.session.add(new_recipe)
            db.session.commit()
        except:
            return 'there was an error adding the recipe'
        
        #Zips three lists that are ingredients, amounts, and units
        ingredients = zip(recipe_ingredients, recipe_amounts, recipe_units)

        #Calls ingredients_add with the tuple from zip
        ingredients_add(ingredients, new_recipe.id)

        steps_add(recipe_steps, new_recipe.id )

        for tags in tag_list:
            if ':' in tags:
                t = tags.split(':')
                found_tag = Tag.query.filter_by(category = t[0].strip(), unit = t[1].strip()).first()
                print(found_tag)
                if found_tag:
                    tag_add(new_recipe.id, found_tag.id)

        return redirect('/')
    else:
        categories = Tag.query.with_entities(Tag.category).distinct()
        tags = Tag.query.all()

        return render_template('addrecipe.html', cats = categories, tags2d = tags)
      



def create_recepie(name, description, portions, user_id, recipe_image):
        recipe = Recipe(
            recipe_title=name,
            recipe_image= recipe_image,
            description=description,
            portions=check_portions(portions),
            user_id=user_id)

        return recipe

def check_portions(number):
     num = int(number)
     if num <= 0:
        return 1
     elif num > 16:
        return 16
     else:
        return num
     