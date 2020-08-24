from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1> hola ~ </h1>"

@app.route("/about")
def about():
    return "<h1> about this thing </h1>"

@app.route("/register", methods=('GET', 'POST'))
def register():
    return "<h1> coming soon </h1>"

@app.route("/login", methods=('GET', 'POST'))
def login():
    return "<h1> coming soon </h1>"