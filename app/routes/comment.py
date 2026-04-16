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
        return render_template('comment.html')

    