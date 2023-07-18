from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'name', 'email', 'password', 'games')
        
user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])