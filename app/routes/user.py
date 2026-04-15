from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from database.db import db
from app.services.models import User
from app.services.models import Recipe

userpage_bp = Blueprint("userpage", __name__)

@userpage_bp.route('/user',methods = ['POST','GET'])
def userpage():
    if request.method == 'POST':
        return redirect('/') # Nothing Post-able added yet! To the homepage with thee!
    else:
        if 'username' in session:
            profile_session = session['username']
            profile_user : User = User.query.filter_by(email=profile_session).first()
            session['name'] = profile_user.name
            if not profile_user.last_name == "":
                session['surname'] = profile_user.last_name
            else:
                if 'surname' in session:
                    session.pop('surname',None)

        return render_template('userpage.html')
    

@userpage_bp.route('/user/edit',methods = ['POST','GET'])
def edit():
    flash('Sorry! I have not yet implemented the edit path!',category='error')
    return render_template('userpage.html')


@userpage_bp.route('/user/recipes',methods = ['POST','GET'])
def recipes():
    if request.method == 'POST':
        return redirect('/') # Nothing Post-able added yet! To the homepage with thee!
    else:
        if not 'username' in session:
            flash('You need to log in to view your recipes!',category='error')
        else:
            flash('You might have recipes, but I have not yet implemented the fetch function!',category='message')
        return render_template('userpage.html')