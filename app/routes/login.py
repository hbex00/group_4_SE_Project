from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from database.db import db
from app.services.models import *
from app.utils.helper_function import *


#go to login page
login_bp = Blueprint("login", __name__)

@login_bp.route('/login', methods=['POST', 'GET'])
def login():
    if 'id' in session:
        return redirect('/')
    
    if request.method == 'GET':
        #include session
        return render_template('loginpage.html')
    
    else:
        try:
            email = request.form['email'].lower()
            password = request.form['password']

            user = User.query.filter_by(email=email).first()
            if user:
                if user.check_hashed_password(password):
                    session_handler(user=user)
                    #should also return session
                    return redirect('/')
                else:
                    return "password hash error"
            else:
                return 'wrong email or password'
                return render_template('loginpage.html')

        except:
            return 'Big Error'
            return render_template('loginpage.html')
