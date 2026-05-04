from flask import Flask, session
from database.db import db
from app.services.models import *

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def session_handler(user):
    session['id'] = user.id
    session['first_name'] = user.name
    session['profile_image'] = user.profile_image
    if not user.last_name == "":
        session['last_name'] = user.last_name
    else:
        session.pop('last_name',None)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS