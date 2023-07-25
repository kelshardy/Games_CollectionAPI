from init import db 
from flask import Blueprint, request
from models.game import Game, game_schema, games_schema 
from models.collection import Collection
from .review_controller import reviews_bp
from flask_jwt_extended import jwt_required
from models.user import User

games_bp = Blueprint('games', __name__, url_prefix='/games')
games_bp.register_blueprint(reviews_bp, url_prefix='/<int:game_id>/reviews')

@games_bp.route('/')
@jwt_required()
def list_games(collection_id):
    stmt = db.select(Collection).filter_by(collection_id=User.user_id)
    collection = db.session.scalar(stmt)
    if collection:   
        stmt = db.select(Game).order_by(Game.title.desc())
        games = db.session.scalars(stmt)
        return games_schema.dump(games)

@games_bp.route('/', methods=['POST'])
def add_game(collection_id):
    body_data = game_schema.load(request.get_json())
    game = Game(
        title=body_data.get('title'),
        platform=body_data.get('platform'),
        genre=body_data.get('genre'),
        multiplayer=body_data.get('multiplayer'),
        release_date=body_data.get('release_date'),
        edition=body_data.get('edition')
    )
    db.session.add(game)
    db.session.commit()
    return game_schema.dump(game), 201