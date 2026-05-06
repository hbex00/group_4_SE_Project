from flask import Flask, render_template, request, redirect, Blueprint, session
from database.db import db
from app.services.models import *
from app.utils.modify_db import *

comment_bp = Blueprint("comment", __name__)

@comment_bp.route('/comment', methods=['POST', 'GET'])
def comment():
    
    if session.get('id') is None:
        return redirect('/login')

    if request.method == 'POST':
             
        recipe_id = request.form.get('recipe_id', type = int)
        found_recipe = Recipe.query.filter_by(id=recipe_id).first()
        
        if recipe_id is None:
            return 'invalid recipe ID'
        elif found_recipe is None:
            return 'Recipe with this ID not found'
        
        content = request.form['comment']

        id = session.get('id')
        user = User.query.filter_by(id=id).first()

        comment_add(recipe_id, content, user.id)
        return redirect('/')
    
    else:
        
        id = request.args.get('c_id', type = int)
        if id is not None:
            recipe = db.session.get(Recipe, id)
        else:
            recipe = None

        return render_template('comment.html', recipe = recipe)

    
@comment_bp.route('/delete-comment', methods=['POST', 'GET'])
def delete_comment():
    if request.method == 'POST':
        if session.get('id') is None:
            return redirect('/login')

        comment_id = request.form.get('comment_id', type = int)
        user_id = session.get('id')

        comment_remove(comment_id, user_id)
        return redirect('/user/recipes')
    else:
        return redirect('/')
    
@comment_bp.route('/edit-comment', methods=['POST', 'GET'])
def edit_comment():
    if request.method == 'POST':
        if session.get('id') is None:
            return redirect('/login')

        comment_id = request.form.get('comment_id', type = int)
        user_id = session.get('id')
        content = request.form.get('content')

        comment_edit(comment_id, content, user_id)
        

        return redirect('/user/recipes')
    else:
        comment_id = request.args.get('comment_id')
        comment = db.session.get(Comment, comment_id)
        recipe = db.session.get(Recipe, comment.recipe_id)

        return render_template('editcomment.html', comment = comment, recipe = recipe)