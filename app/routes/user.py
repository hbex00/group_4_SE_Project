from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from database.db import db
from app.services.models import User
from app.services.models import Recipe

userpage_bp = Blueprint("userpage", __name__)

@userpage_bp.route('/user',methods = ['POST','GET'])
def userpage():
    if request.method == 'POST':
        return redirect('/')
    else:
        try:
            if session.get('id'):
                try:
                    profile_user = User.query.get(session['id'])
                    if not type(profile_user) == User:
                        flash("Your account was not found.",category='error')
                        return render_template('userpage.html')
                    session['first_name'] = profile_user.name
                    if not profile_user.last_name == "":
                        session['last_name'] = profile_user.last_name
                    else:
                        session.pop('last_name',None)
                except RuntimeError as err:
                    flash(message="Unexpected error: " + str(err),category="error")
                    return render_template('userpage.html')
        except RuntimeError as err:
            flash(message="Unexpected error: " + str(err) ,category="error")
        return render_template('userpage.html')
    
    
@userpage_bp.route('/user/edit',methods = ['POST','GET'])
def edit():
    if request.method == 'POST':
        if not 'id' in session:
            flash(message="You must be logged in to edit your account!",category="error")
            return render_template('userpage.html')
        
        user = User.query.get(session.get('id'))
        if not type(user) == User:
            flash("Your account was not found.",category='error')
            return render_template('userpage.html')
        
        first_name    = request.form['first_name']      .strip()
        last_name     = request.form['last_name']       .strip()
        email_address = request.form['email_address']   .strip()
        password1     = request.form['password1']
        password2     = request.form['password2']

        if not (password1 == password2):
            flash(message="Passwords does not match!",category="info")
            return render_template('userpage.html',user=user,edit=True)

        if not email_address == "":
            if not user.check_email_format(email_address):
                flash(message="Unknown formatting for the email-address!",category="info")
                return render_template('userpage.html',user=user,edit=True)
            
        try:
            
            new_user = user

            if not first_name == "":
                new_user.name = first_name

            if not last_name == "":
                new_user.last_name = last_name

            if not email_address == "":
                new_user.email = email_address

            if not password1 == "":
                new_user.set_hashed_password(password1)
                
            db.session.delete(user)
            db.session.add(new_user)
            db.session.commit()

        except RuntimeError as err:
            flash(message="Could not commit user details to database!> " + str(err),category="error")
            return render_template('userpage.html')
        return redirect('/user')
    else:
        if not 'id' in session:
            flash('You must be logged in to edit your account details!',category='error')
            return render_template('userpage.html')
        else:
            try:
                user = User.query.get(session.get('id'))
                if not type(user) == User:
                    flash("Your account was not found.",category='error')
                    return render_template('userpage.html')
                
                return render_template('userpage.html',user=user,edit=True)
            except RuntimeError as err:
                flash(message="Error encountered: " + str(err),category="error")
    return render_template('userpage.html')


@userpage_bp.route('/user/recipes', methods = ['POST','GET'])
def recipes():
    if request.method == 'POST':
        return redirect('/') # Nothing Post-able added yet! To the homepage with thee!
    else:
        if not 'id' in session:
            flash('You need to log in to view your recipes!',category='error')
        else:
            try:
                user = User.query.get(session.get('id'))
                if not type(user) == User:
                    flash("Your account was not found.",category='error')
                    return render_template('userpage.html')

                if not user.recipies:
                    flash("It appears that you have no recipes yet.",category='info')
                    return render_template('userpage.html')

                return render_template('userpage.html',user=user,show_recipes=True)
            except AttributeError or TypeError as err:
                flash("Attribute Error: " + str(err),category='error')
    return render_template('userpage.html')