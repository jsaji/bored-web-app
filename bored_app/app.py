
"""
app.py
- provides the endpoints for consuming and producing
  the web app
"""

from flask import Flask, render_template, Blueprint
import requests

web_app = Flask(__name__)

@web_app.route("/")
def index():
    r = requests.get('https://www.boredapi.com/api/activity')
    activity = r.json()
    return "<h1> hola ~ </h1>"

@web_app.route("/about")
def about():
    return "<h1> about this thing </h1>"

@web_app.route("/register", methods=('GET', 'POST'))
def register():
    return "<h1> coming soon </h1>"

@web_app.route("/login", methods=('GET', 'POST'))
def login():
    return "<h1> coming soon </h1>"

@web_app.route("/profile", methods=('GET', 'POST'))
def profile():
    return "<h1> coming soon </h1>"

@web_app.route("/activitylist", methods=('GET', 'POST'))
def activitylist():
    return "<h1> coming soon </h1>"