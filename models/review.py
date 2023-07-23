from init import db, ma
from marshmallow import fields

class Review(db.Model):
    __tablename__ = 'reviews'
    
    review_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    time_played = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    
    user = db.relationship('User', back_populates='reviews')
    game = db.relationship('Game', back_populates='reviews')
    
class ReviewSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    game = fields.Nested('GameSchema', exclude=['reviews'])
    
    class Meta:
        fields = ('review_id', 'comment', 'time_played', 'rating', 'game')
        
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)