from init import db, ma
from marshmallow import fields

# Creates the User model in the database
class User(db.Model):
    __tablename__ = 'users'
    # Attributes in User model
    user_id = db.Column(db.Integer, primary_key=True)
    # Required input to create an authorised login
    name = db.Column(db.String(100))
    # Email must be unique to create login
    email = db.Column(db.String, nullable=False, unique=True)
    # Login cannot be created without a password
    password = db.Column(db.String, nullable=False)
    
    # The User table has relationships with the Collection and Review models
    collections = db.relationship('Collection', back_populates='user', cascade='all, delete')
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete')
    
# Makes the Schema for User model
class UserSchema(ma.Schema):
    collections = fields.List(fields.Nested('CollectionSchema'))
    
    class Meta:
        fields = ('user_id', 'name', 'email', 'password', 'games')
        
user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])