from flask import Flask, session
from sqlalchemy import select, String, Text, or_
from sqlalchemy.orm import DeclarativeMeta
from database.db import db

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
    

def exact_text_search_table(pattern,orm_class):
    if not pattern:
        raise ValueError("Empty pattern")
    
    if not orm_class:
        raise ValueError("Empty class")
    
    if not isinstance(orm_class, DeclarativeMeta):
        raise TypeError("orm_class must be a SQLAlchemy model")   

    table_text_columns = []
    for column in orm_class.__table__.columns:
        if isinstance(column.type, (String,Text)):
            table_text_columns.append(column)
    if not table_text_columns:
        return []

    column_match_conditions = [column.ilike(pattern) for column in table_text_columns]
    matching_table_query = select(orm_class).where(or_(*column_match_conditions))
    try:
        return db.session.execute(matching_table_query).scalars().all()
    except: raise
    