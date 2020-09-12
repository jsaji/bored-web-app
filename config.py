"""
    config.py
    - settings for the flask application object
"""
import os

class BaseConfig(object):
    # Gets DB connection string, if it's set up
    db_link = os.environ["DB_LINK"]
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = db_link
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False

    