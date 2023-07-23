from init import db 
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.game import Game
from models.review import Review, review_schema, reviews_schema

reviews_bp = Blueprint('reviews', __name__,  url_prefix='/reviews')

@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review(game_id):
    body_data = request.get_json()
    stmt = db.select(Game).filter_by(id=game_id)
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
        return {'error': f'Game not found with id {game_id}'}, 404
    
@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(game_id, review_id):
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        db.session.delete(review)
        db.session.commit()
        return {'message': f'Review for {review.game} was deleted successfully.'}
    else:
        return {'error': f'Review not found for {review.game}'}, 404
    
        