from init import db, ma
from marshmallow import fields

# Creates the Review model for the database
class Review(db.Model):
    __tablename__ = 'reviews'
    # The table attributes
    review_id = db.Column(db.Integer, primary_key=True)
    # Input collected from the User to store in regards to a Game
    comment = db.Column(db.Text)
    time_played = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    # Foreign Keys of Review model
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    # The relations of the Review table link to the User and Game models
    user = db.relationship('User', back_populates='reviews')
    game = db.relationship('Game', back_populates='reviews')
    
# Establishes a Schema for Review model
class ReviewSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    game = fields.Nested('GameSchema')
    
    class Meta:
        fields = ('review_id', 'comment', 'time_played', 'rating', 'game')
        ordered = True
        
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)