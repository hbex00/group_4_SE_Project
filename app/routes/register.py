from flask import Flask, render_template, request, redirect, Blueprint, session, current_app
from database.db import db
from app.services.models import *
from app.utils.helper_function import *
import uuid
from werkzeug.utils import secure_filename
import os

register_bp = Blueprint("register", __name__)

@register_bp.route('/register',methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        first_name = request.form['f_name']
        last_name = request.form['l_name']
        mail = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        file = request.files.get('file')
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_name = str(uuid.uuid4()) + "_" + filename
                UPLOAD_FOLDER = os.path.join(current_app.static_folder, "Bilder", "profile_pics")
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, unique_name))
                profile_image = unique_name
        else:
            profile_image = "default.svg"
        try:
            register_user_database(first_name, last_name, mail.lower(), password1, password2, profile_image = profile_image)
            #after a new user is registerd we put them in the sessin before returning to 
            user = User.query.filter_by(email=mail.lower()).first()
            session_handler(user=user)
            return redirect('/') # Temporary, needs change. Future enhancement.
        except RuntimeError as err:
            return "Error: " + str(err)

    else:
        return render_template('registerpage.html')
    
def register_user_database(name, last_name, mail, password1, password2, profile_image):
    new_user : User
    try:
        new_user = register_user(name, last_name, mail, password1, password2, profile_image)
        try:
            db.session.add(new_user)                    
            db.session.commit()
        except:
            raise RuntimeError('Database Error')
    except RuntimeError as err:
        raise err # passes the caught runtime error upwards.
    


def register_user(name, last_name, mail, password1, password2, profile_image):
    if name.strip() == "":
        raise RuntimeError('Empty Name')
    if password1.strip() == "":
        raise RuntimeError('Empty Password')
    if not("@" in mail and "." in mail):
        raise RuntimeError('Incorrect email format')
    else:
        if password1 == password2:
            if name:
                name = name.lower()
                name = name[:1].upper() + name[1:]
            
            if last_name:
                last_name = last_name.lower()
                last_name = last_name[:1].upper() + last_name[1:]

            if mail:
                mail = mail.lower()

            new_user = User(name=name, last_name=last_name, email=mail, profile_image=profile_image)
            new_user.set_hashed_password(password1)
            return new_user
        else:
            raise RuntimeError('Password Mismatch')
