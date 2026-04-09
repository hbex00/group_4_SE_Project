from flask import Flask, render_template, request, redirect, Blueprint
from database.db import db
from app.services.models import *
from werkzeug.security import generate_password_hash

register_bp = Blueprint("register", __name__)

@register_bp.route('/register',methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 == password2:    
            new_user : User
            new_user(name=username,password=hash_password(password1))
            try:
                db.session.add(new_user)                    
                db.session.commit()
                return redirect('/') # Temporary, needs to be changed. Make issue or something.
            except:
                return 'there was an error'
    else:
        return render_template('registerpage.html')

def hash_password(password):
    return generate_password_hash(password)