from init import db, ma
from marshmallow import fields

class Collection(db.Model):
    __tablename__ = 'collections'
    collection_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users_id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games_id'))
    
    games = db.relationship('Game', back_populates='collection', cascade='all, delete')

class CollectionSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    game = fields.Nested('GameSchema')
    
    class Meta:
        fields = ('collection_id', 'user_id', 'game_id')
        
collection_schema = CollectionSchema
collections_schema = CollectionSchema(many=True)