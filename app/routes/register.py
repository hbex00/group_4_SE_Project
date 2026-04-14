from flask import Flask, render_template, request, redirect, Blueprint
from database.db import db
from app.services.models import *
from app.utils.user import *

register_bp = Blueprint("register", __name__)

@register_bp.route('/register',methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        new_user : User
        try:
            new_user = register_user(username, password1, password2)
        except RuntimeError as err:
            return 'Error: ' + str(err)
        try:
            db.session.add(new_user)                    
            db.session.commit()
            return redirect('/') # Temporary, needs change. Future enhancement.
        except:
            return 'there was an error' # Temporary, needs change. Future enhancement.
    else:
        return render_template('registerpage.html')
    

def register_user(username, password1, password2):
    if username.strip() == "":
        raise RuntimeError('Empty Username')
    if password1.strip() == "":
        raise RuntimeError('Empty Password')
    else:
        if password1 == password2:
            new_user = User(name=username)
            User.create_hashed_password(password1)
            return new_user
        else:
            raise RuntimeError('Password Mismatch')
