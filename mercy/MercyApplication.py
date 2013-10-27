import flask
import mercy.config
from flask.ext.sqlalchemy import SQLAlchemy

class MercyApplication(flask.Flask):
    pass

app = None
db = None

def get_db():
    global db
    if not db:
        db = SQLAlchemy(get_app())
    return db

def get_app():
    global app
    if not app:
        app = MercyApplication("mercy")
        app.config['SQLALCHEMY_DATABASE_URI'] = mercy.config.SQLALCHEMY_URI
    return app
