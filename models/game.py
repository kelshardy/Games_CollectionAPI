from init import db, ma
from marshmallow import fields
import datetime

class Game(db.Model):
    __tablename__ = 'games'
    game_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    release_date = db.Column(db.Date)
    multiplayer = db.Column(db.Boolean)
    edition = db.Column(db.String(100))
    
    platform_id = db.Column(db.String, db.ForeignKey('platforms.id'), nullable=False)
    
    platform = db.relationship('Platform', back_populates='games')
    
class GameSchema(ma.Schema):
    user = fields