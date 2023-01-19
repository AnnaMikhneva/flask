from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)
    education = db.Column(db.Text)
    age = db.Column(db.Integer)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
