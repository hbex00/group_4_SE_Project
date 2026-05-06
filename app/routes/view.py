from flask import Flask, render_template, request, redirect, Blueprint, session
from database.db import db
from app.services.models import *
from sqlalchemy import and_, or_

view_bp = Blueprint("view", __name__)

@view_bp.route('/viewrecipe', methods=['POST', 'GET'])
def view():
    id = request.args.get('recipe_id', type = int)
    recipe = Recipe.query.filter(and_(or_(Recipe.private == False, Recipe.user_id == session.get('id')),Recipe.id == id)).first()
    if not recipe:
        return redirect('/')
    else:
        return render_template('viewrecipe.html', recipe=recipe)