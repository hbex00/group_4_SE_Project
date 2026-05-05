from flask import Flask, session
from sqlalchemy import select, String, Text, or_
from sqlalchemy.orm import DeclarativeMeta
from database.db import db
from app.services.models import *

def search(pattern, filter : dict):
    return_list = list()
    if pattern == None:
        return return_list
    
    if bool(filter):
        if filter['recipe']:
            return_list.extend(text_search_table(pattern, Recipe))

        if filter['user']:
            return_list.extend(text_search_table(pattern, User))
    else:
        raise ValueError("No filter provided")
    
    return return_list

def text_search_table(pattern,orm_class):
    if not pattern:
        raise ValueError("Empty pattern")
    
    if not orm_class:
        raise ValueError("Empty class")
    
    if not isinstance(orm_class, DeclarativeMeta):
        raise TypeError("orm_class must be a SQLAlchemy model")
    
    search_pattern = f"%{pattern}%"    

    table_text_columns = []
    for column in orm_class.__table__.columns:
        if isinstance(column.type, (String,Text)):
            table_text_columns.append(column)
    if not table_text_columns:
        return []

    column_match_conditions = [column.ilike(search_pattern) for column in table_text_columns]
    matching_table_query = select(orm_class).where(or_(*column_match_conditions))
    try:
        return db.session.execute(matching_table_query).scalars().all()
    except: raise
    