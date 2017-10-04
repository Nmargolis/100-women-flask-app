from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, email):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name


# Helper functions

def connect_to_db(app):
    """Connect the database to  Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'postgresql://localhost/emplify')
    db.app = app
    db.init_app(app)



if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    db.create_all()
    exit()


