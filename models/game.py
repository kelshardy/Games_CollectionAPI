from init import db, ma
from marshmallow import fields

class Game(db.Model):
    __tablename__ = 'games'
    game_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    platform = db.Column(db.String(50))
    genre = db.Column(db.String(100))
    multiplayer = db.Column(db.String(50))
    release_date = db.Column(db.Date)
    edition = db.Column(db.String(100), nullable=True)
    
    collections = db.relationship('Collection', back_populates='game', cascade='all, delete')
    reviews = db.relationship('Review', back_populates='game', cascade='all, delete')
class GameSchema(ma.Schema):
    collection = fields.Nested('CollectionSchema')

    class Meta:
        fields = ('game_id', 'title', 'platform', 'genre', 'multiplayer', 'release_date', 'edition')
        
game_schema = GameSchema()
games_schema = GameSchema(many=True)