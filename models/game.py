from init import db, ma
from marshmallow import fields

# Creates the Game model for the database
class Game(db.Model):
    __tablename__ = 'games'
    # The attributes of the Game entity
    game_id = db.Column(db.Integer, primary_key=True)
    # Require input from User - the game information to store
    title = db.Column(db.String(100))
    platform = db.Column(db.String(50))
    genre = db.Column(db.String(100))
    multiplayer = db.Column(db.String(50))
    release_date = db.Column(db.Date)
    edition = db.Column(db.String(100), nullable=True)
    # The Game table relationships 
    collections = db.relationship('Collection', back_populates='game', cascade='all, delete')
    reviews = db.relationship('Review', back_populates='game', cascade='all, delete')

# Schema created for the Game model
class GameSchema(ma.Schema):
    collection = fields.Nested('CollectionSchema')

    class Meta:
        fields = ('game_id', 'title', 'platform', 'genre', 'multiplayer', 'release_date', 'edition')
        
game_schema = GameSchema()
games_schema = GameSchema(many=True)