from flask import Flask, render_template, request, redirect, Blueprint
from database.db import db
from app.services.models import Recipe

modify_bp = Blueprint("modify", __name__)

@modify_bp.route('/modify', methods=['POST', 'GET'])
def modify():
    id = request.args.get('recipe_id', type = int)
    recipe = Recipe.query.get(id)
    if not recipe:
        return redirect('/')
    else:
        return render_template('viewrecipe.html', recipe=recipe)
    