from init import db, ma
from marshmallow import fields

class Collection(db.Model):
    __tablename__ = 'collections'
    collection_id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))
    
    user = db.relationship('User', back_populates='collections')
    game = db.relationship('Game', back_populates='collections')

class CollectionSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    games = fields.Nested('GameSchema')
    
    class Meta:
        fields = ('collection_id', 'label', 'user_id', 'game_id')
        
collection_schema = CollectionSchema()
collections_schema = CollectionSchema(many=True)