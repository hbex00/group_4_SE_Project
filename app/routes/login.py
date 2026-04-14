from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from database.db import db
from app.services.models import *


#go to login page
login_bp = Blueprint("login", __name__)

@login_bp.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect('/')
    
    if request.method == 'GET':
        #include session
        return render_template('loginpage.html')
    
    else:
        try:
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(name=username).first()
            if user:
                if user.check_hashed_password(password):
                    session['username'] = username
                    #should also return session
                    return redirect('/')
            else:
                return 'wrong username or password'
                return render_template('loginpage.html')

        except:
            return 'Big Error'
            return render_template('loginpage.html')
