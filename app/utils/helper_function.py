from flask import Flask, session
from database.db import db
from app.services.models import *

def session_handler(user):
    session['id'] = user.id
    session['first_name'] = user.name
    if not user.last_name == "":
        session['last_name'] = user.last_name
    else:
        session.pop('last_name',None)