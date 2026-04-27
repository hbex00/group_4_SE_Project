from flask import Flask, render_template, request, redirect, session, flash
from app.services.models import *
from app.utils.modify_db import *
from database.db import db

def Create_Tags():

    tag_list = [Tag(category = 'Time',
                    unit = '15 minutes'),
                Tag(category = 'Time',
                    unit = '30 minutes'),
                Tag(category = 'Time',
                    unit = '45 minutes'),
                Tag(category = 'Time',
                    unit = '1 hour'),
                Tag(category = 'Time',
                    unit = '2 hours'),
                Tag(category = 'Complexity',
                    unit = 'Easy'),
                Tag(category = 'Complexity',
                    unit = 'Medium'),
                Tag(category = 'Complexity',
                    unit = 'Hard'),
                Tag(category = 'Complexity',
                    unit = 'GR'),
                Tag(category = 'Spice',
                    unit = '1'),
                Tag(category = 'Spice',
                    unit = '2'),
                Tag(category = 'Spice',
                    unit = '3')]
    
    for tag in tag_list:
        db.session.add(tag)
    
    db.session.commit()