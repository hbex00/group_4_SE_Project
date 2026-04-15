from flask import Flask, render_template, request, redirect, Blueprint
from database.db import db
from app.services.models import *

view_bp = Blueprint("view", __name__)

@view_bp.route('/viewrecipe', methods=['POST', 'GET'])
def view():
    id = request.args.get('recipe_id', type = int)
    recipe = Recipe.query.get(id)
    if not recipe:
        return redirect('/')
    else:
        return render_template('viewrecipe.html', recipe=recipe)