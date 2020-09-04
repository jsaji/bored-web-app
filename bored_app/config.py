"""
    config.py
    - settings for the flask application object
"""
import os

class BaseConfig(object):
    
    db_link = "null" #os.environ["DB_LINK"] or 
    # NEED TO USE ENV VARIABLES HERE
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = db_link
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    