import datetime
from ..app import db, ma



class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'date')  # fields to expose

user_schema = UserSchema()
users_schema = UserSchema(many=True)