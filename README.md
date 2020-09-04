# Bored.

## Project Idea

A web application for when you're bored and looking for something to do.

## Environment Setup & Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies required for development using the `requirements.txt` file in the project's root folder:

```bash
pip install -r requirements.txt
```

### Making database migrations using SQLAlchemy ORM
Create an initial migration file to translate the classes in models.py to SQL that will generate corresponding tables
```bash
python manage.py db migrate
```
Run the migration to upgrade the database with the tables described in the prior step
```bash
python manage.py db upgrade
```

## How To Use The Web App

## Running the API locally

Execute the following bash command from the project root folder to start the API server on `localhost:5000/api/`. Note you need to have Python and all dependencies installed first.
```bash
python appserver.py
```

## Screen Captures

