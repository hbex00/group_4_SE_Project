from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from database.db import db
from app.services.models import *
from app.utils.user import reset_password
from app.utils.helper_function import session_handler
from sqlalchemy import select

reset_bp = Blueprint("reset", __name__)

@reset_bp.route('/reset', methods=['POST', 'GET'])
def passwordReset():
    if request.method == 'GET':
        return render_template('password-reset.html')
    if request.method == 'POST':
        if 'id' in session:
            return redirect('/')
        else:
            email = request.form['email'].lower()
            name = request.form['name']
            new_pass = request.form['password1']
            password_control = request.form['password2']
            new_user = reset_password(email, name, new_pass, password_control)
            if new_user == None:
                return "User not found"
            if isinstance(new_user, str):
                return new_user
            session_handler(new_user)
            return redirect('/')