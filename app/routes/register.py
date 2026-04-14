from flask import Flask, render_template, request, redirect, Blueprint
from database.db import db
from app.services.models import *

register_bp = Blueprint("register", __name__)

@register_bp.route('/register',methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['f_name']
        password1 = request.form['password1']
        password2 = request.form['password2']
        try:
            register_user_database(username, first_name, password1, password2)
            return redirect('/') # Temporary, needs change. Future enhancement.
        except RuntimeError as err:
            return "Error: " + str(err)

    else:
        return render_template('registerpage.html')
    
def register_user_database(username, first_name, password1, password2):
    new_user : User
    try:
        new_user = register_user(username, first_name, password1, password2)
        try:
            db.session.add(new_user)                    
            db.session.commit()
        except:
            raise RuntimeError('Database Error')
    except RuntimeError as err:
        raise err # passes the caught runtime error upwards.
    


def register_user(username, first_name, password1, password2):
    if username.strip() == "":
        raise RuntimeError('Empty Username')
    if password1.strip() == "":
        raise RuntimeError('Empty Password')
    else:
        if password1 == password2:
            new_user = User(name=username, f_name=first_name)
            new_user.set_hashed_password(password1)
            return new_user
        else:
            raise RuntimeError('Password Mismatch')
