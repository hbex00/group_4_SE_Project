from flask import Flask, redirect, Blueprint, session

logout_bp = Blueprint("logout", __name__)

@logout_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('username', None)
    return redirect('/')

