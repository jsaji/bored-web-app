# Bored.

## Project Idea

A web application for when you're bored and looking for something to do. Getting data from the [Bored API](https://www.boredapi.com/), Bored lets you find random activities and save them for later (and mark them as completed too).

The project is built using Python (Flask), HTML and CSS, and interacts with the Bored API and a database.

## Environment Setup & Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies required for development using the `requirements.txt` file in the project's root folder:

```bash
pip install -r requirements.txt
```
It is recommended to use a [virtual environment](https://docs.python.org/3/library/venv.html) to isolate from other projects.

### Making database migrations using SQLAlchemy ORM

NOTE: A database connection string is required as an environment variabled, set as an environment variable by typing into command line:
```
set DB_LINK=mysql://username:password@server:post_number/database_name
```

Create an initial migration file to translate the classes in models.py to SQL that will generate corresponding tables
```
python manage.py db migrate
```
Run the migration to upgrade the database with the tables described in the prior step
```
python manage.py db upgrade
```

## How To Use The Web App

When opened, the web app will take you to the Home page, where you can see a randomly selected activity (below is a short description of the app). From here, you can save the activity for later but you'll need to register/login with an account. Don't worry, if you're taken to login or register, when you come back, you'll see the same activity that you saw before registering/logging in.
On the Saved Activities page, you can see all the activities you have saved. Here you can complete the ones you have done or remove them if you want to.

As at 13/09/2020, the web app can be accessed [here](https://bored-app.azurewebsites.net/).

## Running the API locally

Set database connection string as an environment variable, as in the **Making database migrations using SQLAlchemy ORM** section.

Execute the following bash command from the project root folder to start the API server on `localhost:5000/`. Note you need to have Python and all dependencies installed first.
```bash
python app.py
```

## Screen Captures
Home page:
![Home page](img/main.png)

Saved activities page:
![Saved activities](img/saved.png)

Login page:
![Login](img/login.png)

Register page:
![Register](img/register.png)