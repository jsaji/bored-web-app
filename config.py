"""
    config.py
    - settings for the flask application object
"""
import os

class BaseConfig(object):
    db_link = os.environ["DB_LINK"]
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = db_link
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False

    