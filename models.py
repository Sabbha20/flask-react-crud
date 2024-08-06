from app import db
import datetime

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    
    def __init__(self, name, email):
        self.name = name
        self.email = email