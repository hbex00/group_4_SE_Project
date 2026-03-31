from flask import Flask, render_template, request, redirect, Blueprint
from database.db import db
from app.services.models import Recipe

view_bp = Blueprint("view", __name__)

@view_bp.route('/viewrecipe', methods=['POST', 'GET'])
def view():
    id = request.form.get('recipe_id')
    recipe = Recipe.query.get(id)
    return render_template('viewrecipe.html', recipe=recipe)