
"""
app.py
- provides the endpoints for consuming and producing
  the web app
"""

import requests
from flask import Flask, render_template, request, jsonify, session
from .models import Activity, User, UserActivity, db
from sqlalchemy import exc
from flask_session import Session

web_app = Flask(__name__)
web_app.config.from_object('bored_app.config.BaseConfig')
db.init_app(web_app)
Session(web_app)
BASE_URL = 'https://www.boredapi.com/api/activity'

@web_app.route("/")
def index():
    """ Home page """
    title = "Bored?"
    subtitle = "Find things to kill your boredom!"
    if session.get('temp_activity_id'):
        temp_activity_id = session['temp_activity_id']
        session.pop('temp_activity_id', None)
        r = requests.get(BASE_URL, params={'key':temp_activity_id})
    else:
        r = requests.get(BASE_URL)
    activity_data = map_activity_model(r.json())
    activity_data['activity_type'] = activity_data['activity_type'].capitalize()
    activity_data['accessibility'] = int(round(activity_data['accessibility'] * 10))
    activity_data['price'] = int(round(activity_data['price'] * 100))
    activity = Activity(**activity_data)
    if session.get('user_id'):
        user_id = session['user_id']
    else:
        user_id = None
    return render_template("index.html", activity=activity, user_id=user_id, title=title, subtitle=subtitle)


@web_app.route("/register", methods=['GET', 'POST'])
def register():
    """ Register page for new users """
    if request.method == 'GET':
        return render_template("register.html", title="Register")
    
    try:
        data = request.form
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        session['logged_in'] = True
        session['user_id'] = user.user_id
        session['email'] = data['email']
        return index()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return register()


@web_app.route("/login", methods=['GET', 'POST'])
def login():
    """ Login page for existing users """
    if request.method == 'GET':
        return render_template("login.html", email='', title="Login")
    else:
        data = request.form
        valid_user = User.authenticate(**data)

        if not valid_user:
            email = ''
            if data.get('email'): email = data['email']
            return render_template("login.html", email=email)

        user = User.query.filter_by(email=data['email']).first()
        session['logged_in'] = True
        session['user_id'] = user.user_id
        session['email'] = data['email']
        return index()

@web_app.route("/logout", methods=['GET'])
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    session.pop('user_id', None)
    session.pop('temp_activity_id', None)
    return index()

@web_app.route("/profile", methods=['GET'])
def profile():
    """ Profile page for existing users to view their details """
    if session.get('user_id') and session.get('logged_in'):
        user = User.query.get(session['user_id'])
        return render_template("profile.html", user=user, title="My Profile")
    return login()


@web_app.route("/profile/edit", methods=['GET', 'POST'])
def edit_profile():
    """ Profile page for existing users to edit their details """
    return "<h1> coming soon </h1>"


@web_app.route("/activity_list", methods=['GET', 'POST'])
def activity_list():
    """ Activity list page for users to see the activities they have saved """
    if session.get('user_id'):
        title = "Saved Activities"
        subtitle = "Add more things to your list and complete them"
        user_id = session['user_id']
        results = db.session.query(User, UserActivity, Activity).\
                    filter(User.user_id==UserActivity.user_id).\
                    filter(UserActivity.activity_id==Activity.activity_id).\
                    filter(User.user_id==user_id).\
                    all()
        activities = []
        user_activities = []
        for u, ua, a in results:
            user_activities.append(ua.to_dict())
            activities.append(a.to_dict())
            print(ua.to_dict())
        return render_template('activity_list.html', activities=activities, user_activities=user_activities, title=title, subtitle=subtitle)

    return login()


@web_app.route("/activity_list/add", methods=['POST'])
def add_activity():
    """ Add activity to user's list of saved activities """
    try:
        data = request.form
        if data.get('activity_id'):
            session['temp_activity_id'] = data['activity_id']
            if session.get('user_id'):
                user_activity = UserActivity.query.filter_by(activity_id=data['activity_id'], user_id=session['user_id']).first()
                if user_activity is None:
                    user_activity = UserActivity(activity_id=data['activity_id'], user_id=session['user_id'])
                    activity = Activity.query.get(data['activity_id'])
                    if activity is None:
                        activity = Activity(**data)
                        db.session.add(activity)
                        db.session.commit()
                    db.session.add(user_activity)
                    db.session.commit()
            else:
                session['temp_activity_id'] = activity.activity_id
                return login()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(e.args)
    except Exception as e:
        print(e.args)
    return index()


@web_app.route("/activity_list/remove", methods=['POST'])
def remove_activity():
    """ Remove activity from user's list of saved activities """
    try:
        data = request.form
        if data.get('user_activity_id'):
            user_activity = UserActivity.query.get(data['user_activity_id'])
            if user_activity is not None:
                print(user_activity.to_dict())
                db.session.delete(user_activity)
                db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(e.args)
    except Exception as e:
        print(e.args)

    return activity_list()


@web_app.route("/activity_list/complete", methods=['POST'])
def complete_activity():
    """ Complete an activity on user's list of saved activities """
    try:
        data = request.form
        if data.get('user_activity_id'):
            user_activity = UserActivity.query.get(data['user_activity_id'])
            if user_activity is not None:
                user_activity.is_completed = not user_activity.is_completed
                db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(e.args)
    except Exception as e:
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
