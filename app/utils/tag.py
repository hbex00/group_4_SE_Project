from flask import Flask, render_template, request, redirect, session, flash
from app.services.models import *
from app.utils.modify_db import *
from database.db import db

def Create_Tags():
    Tag1 = Tag(name = 'Time',
               amount = 15)
    Tag2 = Tag(name = 'Time',
               amount = 30)
    
    db.session.add(Tag1)
    db.session.add(Tag2)
    db.session.commit()