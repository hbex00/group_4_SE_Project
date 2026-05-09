from flask import Flask, render_template, request, redirect, Blueprint, current_app, session
from database.db import db
from app.services.models import *
from app.utils.modify_db import *
from app.utils.tag import *
from app.utils.helper_function import *
import uuid
from werkzeug.utils import secure_filename
import os
from sqlalchemy import or_, and_

modify_bp = Blueprint("modify", __name__)

@modify_bp.route('/modify', methods=['POST', 'GET'])
def modify():
    
    # when geting input from user we change all the inputs for a recipe in the database
    if request.method == 'POST' :
        id = request.form.get('recipe_id', type = int)
        recipe = Recipe.query.get(id)
        try:
            if request.form['title'].strip() != "":
                recipe.recipe_title = request.form['title'] 
        except:
            recipe.recipe_title = recipe.recipe_title
        recipe.description = request.form['description']
        recipe.portions = request.form['portions']
        recipe.private = True if 'private' in request.form else False

        tag_list = request.form.getlist('tag[]')

        file = request.files.get('file')

        if file and file.filename != '':

            if allowed_file(file.filename):

                if recipe.recipe_image and recipe.recipe_image != None:
                    old_path = os.path.join(current_app.static_folder, "Bilder", "recipe_pics",recipe.recipe_image)
                    if os.path.exists(old_path):
                        os.remove(old_path)

                filename = secure_filename(file.filename)
                unique_name = str(uuid.uuid4()) + "_" + filename

                UPLOAD_FOLDER = os.path.join(current_app.static_folder, "Bilder", "recipe_pics")
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, unique_name))
                recipe.recipe_image = unique_name

    # we delete all the lists of ingredents, steps and tags
        Ingredient.query.filter_by(recipe_id = id).delete()
        Step.query.filter_by(recipe_id = id).delete()
        RecipeTag.query.filter_by(recipe_id= id).delete()
        db.session.commit()

        ingredients = zip(
            request.form.getlist('ingredients[]'),
            request.form.getlist('amount[]'),
            request.form.getlist('unit[]')
            )

        steps = request.form.getlist("step[]")

    # then uses the functions to add them back in 
        ingredients_add(ingredients, id)
        steps_add(steps, id)

        for tags in tag_list:
            if ':' in tags:
                t = tags.split(':')
                found_tag = Tag.query.filter_by(category = t[0].strip(), unit = t[1].strip()).first()
                print(found_tag)
                if found_tag:
                    tag_add(id, found_tag.id)


        return redirect('/viewrecipe')
    
    id = request.args.get('recipe_id', type = int)
    recipe = Recipe.query.filter(and_(Recipe.user_id == session.get('id'),Recipe.id == id)).first()

    if recipe == None:
        return redirect('/')

    categories = Tag.query.with_entities(Tag.category).distinct()
    tags = Tag.query.all()
    
    return render_template('modify.html', recipe=recipe, cats = categories, tags2d = tags)