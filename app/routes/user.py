from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from app.services.models import User
from app.utils.user import check_user,update_user

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
        
        session['first_name'] = profile_user.name
        if not profile_user.last_name == "":
            session['last_name'] = profile_user.last_name
        else:
            session.pop('last_name',None)
        return render_template(page)
    
@userpage_bp.route('/user/edit',methods = ['POST','GET'])
def user_edit():
    if request.method == 'POST':
        return update_user(request.form.to_dict(),page,flashes,path)
    else:
        user = check_user(page,flashes)
        return render_template(page,user=user,edit=True)


@userpage_bp.route('/user/recipes', methods = ['POST','GET'])
def user_recipes():
    if request.method == 'POST':
        return redirect('/') # Nothing Post-able added yet! To the homepage with thee!
    else:
        user = check_user(page,flashes)
        if not user.recipies:
            flash("It appears that you have no recipes yet.",category='info')
            return render_template(page)
        return render_template(page,user=user,show_recipes=True)