from flask import Flask, render_template, request, redirect, Blueprint, session
from database.db import db
from app.services.models import *
from app.utils.modify_db import *

review_bp = Blueprint("review", __name__)

@review_bp.route('/review', methods=['POST', 'GET'])
def review():
    
    if session.get('username') is None:
        return redirect('/login')

    if request.method == 'POST':
        
        return redirect('/')
    else:
        return render_template('review.html')