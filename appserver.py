"""
appserver.py
- creates an application instance and runs the dev server
"""

from bored_app.app import web_app
from bored_app.models import db

if __name__ == '__main__':
    app = web_app
    app.config.from_object('bored_app.config.BaseConfig')
    db.init_app(app)
    app.run()
