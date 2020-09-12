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

# Intialises the app
web_app = Flask(__name__)
web_app.config.from_object('bored_app.config.BaseConfig')
db.init_app(web_app)
Session(web_app)
BASE_URL = 'https://www.boredapi.com/api/activity'

@web_app.route("/")
def index():
    """ Home page """
    try:
        # Sets title and subtitle to be used on the page
        title = "Bored?"
        subtitle = "Find things to kill your boredom!"
        if session.get('temp_activity_id'):
            # If there was an activity id in storage, get this specific one
            # (e.g. finding one, then having to log in will keep the activity first seen)
            temp_activity_id = session['temp_activity_id']
            session.pop('temp_activity_id', None)
            r = requests.get(BASE_URL, params={'key':temp_activity_id})
        else:
            # Else get a random activity
            r = requests.get(BASE_URL)
        # Maps returned data to the fields of the Activity model we use (for consistency)
        activity_data = map_activity_model(r.json())
        activity_data['activity_type'] = activity_data['activity_type'].capitalize()
        activity_data['accessibility'] = int(round(activity_data['accessibility'] * 10))
        activity_data['price'] = int(round(activity_data['price'] * 100))
        # Returns template
        return render_template("index.html", activity=activity_data, title=title, subtitle=subtitle)
    except Exception as e:
        # If an error occurs, returns an error page
        return error(e.args)

@web_app.route("/register", methods=['GET', 'POST'])
def register():
    """ Register page for new users """
    error_msgs = []
    email = ''
    try:
        # If GETting the page, return it
        if request.method == 'GET':
            return render_template("register.html", title="Register")

        # We're here if it's a POST request
        # Gets POST form data and checks email and password fields
        # If there are any issues, return register page with error messages
        data = request.form
        if not data.get("email"):
            error_msgs.append("Please enter an email.")
        else:
            email = data['email']
        if data.get("password"):
            password = data['password']
            if len(password) < 6:
                error_msgs.append("Password must have at least 8 characters.")
            if not data.get('confirm_password'): 
                error_msgs.append("Please confirm password.")
            elif data['confirm_password'] != password:
                error_msgs.append("Passwords do not match.")
        else:
            error_msgs.append("Please enter a password.")
        # If there are no errors, create the user, log them in and return to home page
        if not len(error_msgs):
            user = User(email=email, password=password)
            db.session.add(user)
            db.session.commit()
            session['logged_in'] = True
            session['user_id'] = user.user_id
            session['email'] = data['email']
            return index()
    except exc.SQLAlchemyError as e:
        # In case of a DB error, roll it back
        db.session.rollback()
    except Exception as e:
        # If an error occurs, returns an error page
        return error(e.args)
    # This point is reached if there are issues with email or password
    return render_template("register.html", title="Register", error_msgs=error_msgs, email=email)


@web_app.route("/login", methods=['GET', 'POST'])
def login():
    """ Login page for existing users """
    try:
        error_msgs = []
        # If GETting the page, return it
        if request.method == 'GET':
            return render_template("login.html", title="Login")

        # We're here if it's a POST request
        # Gets POST form data and authenticates email/password combination
        data = request.form
        user = User.authenticate(**data)

        # If they're a valid user, store useful information in the session
        if user:
            session['logged_in'] = True
            session['user_id'] = user.user_id
            session['email'] = data['email']
            return index()
        # Return page with error message (and value of email field so it doesn't have to be retyped)
        error_msgs.append("The email or password is incorrect.")
        email = data['email'] if data.get('email') else ''
        return render_template("login.html", email=email, title="Login", error_msgs=error_msgs)
    except Exception as e:
        # If an error occurs, returns an error page
        return error(e.args)

@web_app.route("/logout", methods=['GET'])
def logout():
    try:
        # Remove any session data that was stored
        session.pop('logged_in', None)
        session.pop('email', None)
        session.pop('user_id', None)
        session.pop('temp_activity_id', None)
        return index()
    except Exception as e:
        # If an error occurs, returns an error page
        return error(e.args)

@web_app.route("/activity_list", methods=['GET', 'POST'])
def activity_list():
    """ Activity list page for users to see the activities they have saved """
    try:
        if session.get('user_id'):
            # If user is logged in, get any saved activities they may have
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
            # Iterates over the set of tuples returned
            for u, ua, a in results:
                user_activities.append(ua.to_dict())
                activities.append(a.to_dict())
            # Returns page filled with saved activities
            return render_template('activity_list.html', activities=activities, user_activities=user_activities, title=title, subtitle=subtitle)
    except Exception as e:
        # If an error occurs, returns an error page
        return error(e.args)
    # This point is reached if user attempts to reach page but is not logged in
    return login()


@web_app.route("/activity_list/add", methods=['POST'])
def add_activity():
    """ Add activity to user's list of saved activities """
    try:
        # Gets form data and checks for activity_id
        data = request.form
        if data.get('activity_id'):
            # If user is logged in, check if they already have saved this activity
            if session.get('user_id'):
                user_activity = UserActivity.query.filter_by(activity_id=data['activity_id'], user_id=session['user_id']).first()
                # If it hasn't already been saved, save it
                if user_activity is None:
                    user_activity = UserActivity(activity_id=data['activity_id'], user_id=session['user_id'])
                    activity = Activity.query.get(data['activity_id'])
                    # If the relevant activity does not exist in the DB, create it too
                    if activity is None:
                        activity = Activity(**data)
                        db.session.add(activity)
                        db.session.commit()
                    db.session.add(user_activity)
                    db.session.commit()
            else:
                # If not logged in, store the id of the current activity and redirect to login
                session['temp_activity_id'] = data['activity_id']
                return login()
    except exc.SQLAlchemyError as e:
        # In case of a DB error, roll it back
        db.session.rollback()
    except Exception as e:
        # If an error occurs, returns an error page
        return error(e.args)
    # Go back to home page
    return index()


@web_app.route("/activity_list/remove", methods=['POST'])
def remove_activity():
    """ Remove activity from user's list of saved activities """
    try:
        # Gets form data and checks for user_activity_id
        data = request.form
        if data.get('user_activity_id'):
            # Checks if it exists in the DB and deletes it if it does exist
            user_activity = UserActivity.query.get(data['user_activity_id'])
            if user_activity is not None:
                db.session.delete(user_activity)
                db.session.commit()
    except exc.SQLAlchemyError as e:
        # In case of a DB error, roll it back
        db.session.rollback()
    except Exception as e:
        # If an error occurs, returns an error page
        return error(e.args)
    # Go back to activity list page
    return activity_list()


@web_app.route("/activity_list/complete", methods=['POST'])
def complete_activity():
    """ Complete/uncomplete an activity on user's list of saved activities """
    try:
        # Gets form data and checks for user_activity_id
        data = request.form
        if data.get('user_activity_id'):
            user_activity = UserActivity.query.get(data['user_activity_id'])
            # Checks if it exists in the DB, and inverts the is_completed flag
            if user_activity is not None:
                user_activity.is_completed = not user_activity.is_completed
                db.session.commit()
    except exc.SQLAlchemyError as e:
        # In case of a DB error, roll it back
        db.session.rollback()
    except Exception as e:
        # If an error occurs, returns an error page
        return error(e.args)
    # Go back to activity list page
    return activity_list()

def error(error_msg):
    """ Returns an error page """
    return render_template('error.html', error=error_msg, title="ERROR")

def map_activity_model(raw_activity):
    """ Maps request data to the fields defined for the Activity model """
    return {
        'activity_id': raw_activity['key'],
        'description': raw_activity['activity'],
        'activity_type':  raw_activity['type'],
        'participants':  raw_activity['participants'],
        'accessibility':  raw_activity['accessibility'],
        'price':  raw_activity['price'],
        'link': raw_activity['link']
    }