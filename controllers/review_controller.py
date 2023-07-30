from init import db 
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.game import Game
from models.collection import Collection
from models.review import Review, review_schema, reviews_schema

reviews_bp = Blueprint('reviews', __name__)

# Function to shows the reviews on a certain game with this route and method
@reviews_bp.route('/', methods=['GET'])
@jwt_required()
def get_reviews(collection_id, game_id):
    stmt = db.select(Collection).filter_by(collection_id=collection_id)
    collection = db.session.scalar(stmt)
    if collection:
        stmt = db.select(Game).filter_by(game_id=game_id)
        game = db.session.scalar(stmt)
        if game: 
            stmt = db.select(Review)
            reviews = db.session.scalars(stmt)
            return reviews_schema.dump(reviews), 201

# Allows the user to create a review on a particular game 
@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review(collection_id, game_id):
    body_data = request.get_json()
    stmt = db.select(Game).filter_by(game_id=game_id)
    game = db.session.scalar(stmt)
    if game:
        review = Review(
            comment=body_data.get('comment'),
            time_played=body_data.get('time_played'),
            rating=body_data.get('rating'),
            user_id=get_jwt_identity(),
            game=game
        )
        
        db.session.add(review)
        db.session.commit()
        return review_schema.dump(review), 201
    else:
        return {'error': f'Game not found with id {Game.game_id}'}, 404
  
# Gives the User the ability to remove a review from a game  
@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(collection_id, game_id, review_id):
    stmt = db.select(Collection).filter_by(collection_id=collection_id)
    collection = db.session.scalar(stmt)
    if collection:
        stmt = db.select(Game).filter_by(game_id=game_id)
        game = db.session.scalar(stmt)
        if game: 
            stmt = db.select(Review).filter_by(review_id=review_id)
            review = db.session.scalar(stmt)
            if review:
                db.session.delete(review)
                db.session.commit()
                return {'message': f'Review ID {review_id} was deleted successfully.'}
            else:
                return {'error': f'Review not found for ID {review_id}'}, 404

# The User can update/change information within an existing review
@reviews_bp.route('/<int:review_id>', methods=['PUT', 'PATCH'])
def update_review(collection_id, game_id, review_id):
    stmt = db.select(Collection).filter_by(collection_id=collection_id)
    collection = db.session.scalar(stmt)
    if collection:
        stmt = db.select(Game).filter_by(game_id=game_id)
        game = db.session.scalar(stmt)
        if game:
            body_data = review_schema.load(request.get_json(), partial=True)
            stmt = db.select(Review).filter_by(review_id=review_id)
            review = db.session.scalar(stmt)
            if review: 
                review.comment = body_data.get('comment')
                review.time_played = body_data.get('time_played')
                review.rating = body_data.get('rating')
                db.session.commit()
                return review_schema.dump(review)
            else:
                return {'error': f'Review ID {review_id} could not be found'}, 404
            