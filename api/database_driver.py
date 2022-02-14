from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

UPLOADS = os.path.abspath(f'{os.getcwd()}/uploads/')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['UPLOAD_FOLDER'] = UPLOADS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rfid = db.Column(db.String(64), nullable=False)
    barcode = db.Column(db.String(64), nullable=False)
    temperatures = db.relationship('Temperature', backref='owner')

class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    temp = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))