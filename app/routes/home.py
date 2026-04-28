from flask import Flask, render_template, request, redirect, Blueprint
from database.db import db
from app.services.models import *
from app.utils.tag import *

#this creates a new blueprint to use
home_bp = Blueprint("home", __name__)

@home_bp.route('/', methods=['POST', 'GET'])
def home():
    recipe = Recipe.query.all()
    
    tag = Tag.query.count()
    if tag == 0:
        Create_Tags()

    tag = Tag.query.all()
    return render_template('homepage.html', recipies = recipe, tags = tag)
        