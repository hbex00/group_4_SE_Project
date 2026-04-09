from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from database.db import db
from app.services.models import *
from werkzeug.security import check_password_hash


#go to login page
login_bp = Blueprint("login", __name__)


def check_password(user_password, password):
    return check_password_hash(user_password, password)


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
            if user and check_password(user.password, password):
                session['username'] = username
                #should also return session
                return redirect('/')
            else:
                return 'wrong username or password'
                return render_template('loginpage.html')

        except:
            return 'Big Error'
            return render_template('loginpage.html')
