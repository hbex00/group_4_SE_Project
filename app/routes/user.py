from flask import Flask, render_template, request, redirect, Blueprint, session, flash,current_app
from app.services.models import User
from app.utils.user import check_user,update_user
from app.utils.helper_function import *
import uuid
from werkzeug.utils import secure_filename
import os

userpage_bp = Blueprint("userpage", __name__)

#Page variables
page = 'userpage.html'
path = '/user'
flashes = True

@userpage_bp.route('/user',methods = ['POST','GET'])
def userpage():
    if request.method == 'POST':
        return redirect('/')
    else:
        profile_user = check_user(page,flashes)
        if not type(profile_user) == User:
            return profile_user
        session_handler(user=profile_user)
        return render_template(page)
    
@userpage_bp.route('/user/edit',methods = ['POST','GET'])
def user_edit():

    user = check_user(page,flashes)
    if not type(user) == User:
            return user

    if request.method == 'POST':

        file = request.files.get('file')

        if file and file.filename != '':

            if allowed_file(file.filename):

                if user.profile_image and user.profile_image != "default.svg":
                    old_path = os.path.join(current_app.static_folder, "Bilder", "profile_pics",user.profile_image)
                    if os.path.exists(old_path):
                        os.remove(old_path)

                filename = secure_filename(file.filename)
                unique_name = str(uuid.uuid4()) + "_" + filename

                UPLOAD_FOLDER = os.path.join(current_app.static_folder, "Bilder", "profile_pics")
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, unique_name))
                user.profile_image = unique_name

        action = update_user(request.form.to_dict(),page,flashes,path)
        return action
        
    return render_template(page,user=user,edit=True)


@userpage_bp.route('/user/recipes', methods = ['POST','GET'])
def user_recipes():
    if request.method == 'POST':
        return redirect('/') # Nothing Post-able added yet! To the homepage with thee!
    else:
        user = check_user(page,flashes)
        if not type(user) == User:
            return user
        
        if not user.recipies and not user.reviews and not user.comments:
            flash("It appears that you have no actions yet.",category='info')
            return render_template(page)
        return render_template(page,user=user,show_recipes=True)