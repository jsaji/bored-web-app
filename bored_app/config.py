"""
    config.py
    - settings for the flask application object
"""
import os

class BaseConfig(object):
    f = open('bored_app/DB_LINK.txt', 'r')
    db_link = f.read() #os.environ["DB_LINK"]
    f.close() 
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = db_link
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    