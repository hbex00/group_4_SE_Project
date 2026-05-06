from flask import Flask, render_template, request, redirect, Blueprint, session
from database.db import db
from app.services.models import *
from app.utils.tag import *
from sqlalchemy import or_

#this creates a new blueprint to use
home_bp = Blueprint("home", __name__)

@home_bp.route('/', methods=['POST', 'GET'])
def home():
    # all recipies that are not private or belongs to the current user
    recipe = Recipe.query.filter(or_(Recipe.private == False, Recipe.user_id == session.get('id'))).all()
    
    tag = Tag.query.count()
    if tag == 0:
        Create_Tags()

    tag = Tag.query.all()
    return render_template('homepage.html', recipies = recipe, tags = tag)
        