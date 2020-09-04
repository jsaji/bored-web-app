
"""
app.py
- provides the endpoints for consuming and producing
  the web app
"""

import requests
from flask import Flask, render_template, request, jsonify
from .models import Activity, User, UserActivity, db
from sqlalchemy import exc

web_app = Flask(__name__)
web_app.config.from_object('bored_app.config.BaseConfig')
db.init_app(web_app)

@web_app.route("/")
def index():
    """ Home page """
    r = requests.get('https://www.boredapi.com/api/activity')
    activity_data = map_activity_model(r.json())
    activity = Activity(**activity_data)
    return render_template("index.html", activity=activity)


@web_app.route("/about")
def about():
    """ About page with info about the app """
    return "<h1> about this thing </h1>"


@web_app.route("/register", methods=['GET', 'POST'])
def register():
    """ Register page for new users """
    if request.method == 'GET':
        return "<h1> coming soon </h1>"
    else:
        try:
            data = request.get_json()
            user = User(**data)
            db.session.add(user)
            db.session.commit()
            return jsonify(user.to_dict), 201
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'message': e.args}), 500


@web_app.route("/login", methods=['GET', 'POST'])
def login():
    """ Login page for existing users """
    if request.method == 'GET':
        return "<h1> coming soon </h1>"
    else:
        data = request.get_json()
        user = User.authenticate(**data)

        if not user:
            return jsonify({ 'message': 'Invalid login details', 'authenticated': False }), 401
        
        return 200

@web_app.route("/profile", methods=['GET'])
def profile():
    """ Profile page for existing users to view their details """
    return "<h1> coming soon </h1>"


@web_app.route("/profile/edit", methods=['GET', 'POST'])
def edit_profile():
    """ Profile page for existing users to edit their details """
    return "<h1> coming soon </h1>"


@web_app.route("/activity_list", methods=['GET', 'POST'])
def activity_list():
    """ Activity list page for users to see the activities they have saved """
    return "<h1> coming soon </h1>"


@web_app.route("/activity_list/add", methods=['POST'])
def add_activity():
    """ Add activity to user's list of saved activities """
    try:
        data = request.get_json()
        user_activity = UserActivity(**data)
        db.session.add(user_activity)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(e.args)
    return index()


@web_app.route("/activity_list/remove", methods=['POST'])
def remove_activity():
    """ Remove activity from user's list of saved activities """
    try:
        data = request.get_json()
        user_activity = UserActivity(**data)
        db.session.remove(user_activity)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(e.args)

    return activity_list()


@web_app.route("/activity_list/complete", methods=['POST'])
def complete_activity():
    """ Complete an activity on user's list of saved activities """
    try:
        data = request.get_json()
        user_activity = UserActivity(**data)
        user_activity.is_completed = True
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(e.args)

    return activity_list()

def map_activity_model(raw_activity):
    return {
        'activity_id': raw_activity['key'],
        'description': raw_activity['activity'],
        'activity_type':  raw_activity['type'],
        'participants':  raw_activity['participants'],
        'accessibility':  raw_activity['accessibility'],
        'price':  raw_activity['price'],
        'link': raw_activity['link']
    }