from flask import Flask, render_template, request, redirect, Blueprint
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from app.services.models import User

class User(): # Extends User from models.py with additional functionality

    def create_hashed_password(self, password):
        self.password = generate_password_hash(password)

    def check_hashed_password(self,hashed_password):
        return check_password_hash(self.password,hashed_password)