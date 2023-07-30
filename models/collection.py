from init import db, ma
from marshmallow import fields

# The Collection model creates a table in the database that requires an existing User to login
class Collection(db.Model):
    __tablename__ = 'collections'
    # The attributes that make up a Collection
    collection_id = db.Column(db.Integer, primary_key=True)
    # Required User input
    label = db.Column(db.String(100))
    # Foreign Keys of the Collection model
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))
    # Relationships between existing tables of the database
    user = db.relationship('User', back_populates='collections')
    game = db.relationship('Game', back_populates='collections')

# Creates the Schema for Collection model
class CollectionSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    games = fields.Nested('GameSchema')
    
    class Meta:
        fields = ('collection_id', 'label', 'user_id', 'game_id')
        
collection_schema = CollectionSchema()
collections_schema = CollectionSchema(many=True)