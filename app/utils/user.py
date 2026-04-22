from flask import Flask, render_template, request, redirect, session, flash
from app.services.models import User
from app.services.models import Recipe
from database.db import db

def check_user(page : str, flash_message : bool):
    if not page:
        page = 'homepage.html'
    if not flash_message:
        flash_message = False

    if session.get('id'):
        try:
            profile_user = User.query.get(session['id'])
            if not type(profile_user) == User:
                if flash_message:
                    flash("Your account was not found.",category='error')
                if page:
                    return render_template(page)
                else:
                    raise RuntimeError("ID-token Error")
            else:
                return profile_user
            

        except RuntimeError as err:
            if flash_message:
                flash("There was an unexpected error: " + str(err),category="error")
            print("Unexpected Error: " + str(err))
            if page:
                return render_template(page)
            else:
                raise RuntimeError("Database Error")
    else:
        if flash_message:
            flash("You must be logged in to access this feature.")
        if page:
            return render_template(page)
        else:
            raise RuntimeError("ID-token Error")
        
def user_input_acceptance(args :dict):
    if args['first_name']:
        if len(args['first_name'].strip()) > 40:
            return False
    if args['last_name']:
        if len(args['last_name'].strip()) > 40:
            return False
    if args['password1']:
        if len(args['password1']) > 40:
            return False
    if args['password2']:
        if len(args['password2']) > 40:
            return False
    if args['email_address']:
        if len(args['email_address'].strip()) > 60:
            return False
        if check_if_email_exist(args['email_address']):
            return False
    return True

def check_if_email_exist(email_address :str):
    if User.query.filter_by(email=email_address.lower()).first():
        return True
    return False
    
def update_user(args :dict, page :str, flashes :bool, url_path :str):
    if not url_path:
        url_path = '/'
    if not page:
        page = 'homepage.html'
    if not flashes:
        flashes = False

    user = check_user(page,flashes)
    if not user_input_acceptance(args):
        if flashes:
            flash(message="Input not accepted!",category="info")
        if page == 'userpage.html':
            return render_template(page,user=user,edit=True)
        elif page:
            return render_template(page)
        raise RuntimeError("Size Error")
    
    first_name    = args['first_name']      .strip()
    last_name     = args['last_name']       .strip()
    email_address = args['email_address']   .strip()
    password1     = args['password1']
    password2     = args['password2']

    if first_name:
        first_name = first_name.lower()
        first_name = first_name[:1].upper() + first_name[1:]
    if last_name:    
        last_name = last_name.lower()
        last_name = last_name[:1].upper() + last_name[1:]
    if email_address:
        email_address = email_address.lower()

    if not (password1 == password2):
        if flashes:
            flash(message="Passwords does not match!",category="info")
        if page == 'userpage.html':
            return render_template(page,user=user,edit=True)
        elif page:
            return render_template(page)
        raise RuntimeError("Password Error")

    if not email_address == "":
        if not user.check_email_format(email_address):
            if flashes:
                flash(message="Unknown formatting for the email-address!",category="info")
            if page == 'userpage.html':
                return render_template(page,user=user,edit=True)
            elif page:
                return render_template(page)        
            raise RuntimeError("Email-Format Error")
        
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

    except Exception as err:
        if flashes:
            flash(message="Could not commit user details to database! " + str(err),category="error")
        if page:
            return render_template(page)  
        raise RuntimeError("Database Error",args=str(err)) 
    
    return redirect(url_path)
