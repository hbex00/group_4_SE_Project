from flask import Flask, render_template, request, redirect, Blueprint, session
from database.db import db
from app.services.models import *
from app.utils.modify_db import *

comment_bp = Blueprint("comment", __name__)

@comment_bp.route('/comment', methods=['POST', 'GET'])
def comment():
    
    if session.get('username') is None:
        return redirect('/login')

    if request.method == 'POST':
        try: 
            recipe_id = int(request.form['recipe_id'])
        except:
            return 'invalid recipe id'
        content = request.form['comment']

        username = session.get('username')
        user = User.query.filter_by(name=username).first()

        comment_add(recipe_id, content, user.id)
        return redirect('/')
    
    else:
        return render_template('comment.html')

    