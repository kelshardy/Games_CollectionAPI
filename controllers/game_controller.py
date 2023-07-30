from init import db 
from flask import Blueprint, request
from models.game import Game, game_schema, games_schema 
from models.collection import Collection
from .review_controller import reviews_bp
from flask_jwt_extended import jwt_required
from models.user import User

games_bp = Blueprint('games', __name__, url_prefix='/games')
games_bp.register_blueprint(reviews_bp, url_prefix='/<int:game_id>/reviews')

# lists all the games stored within a collection
@games_bp.route('/')
@jwt_required()
def list_games(collection_id):
    stmt = db.select(Collection).filter_by(collection_id=collection_id)
    collection = db.session.scalar(stmt)
    if collection:   
        stmt = db.select(Game).order_by(Game.title.desc())
        games = db.session.scalars(stmt)
        return games_schema.dump(games)

# function to show an individual game within a collection
@games_bp.route('/<int:game_id>', methods=['GET'])
@jwt_required()
def get_one_game(collection_id, game_id):
    stmt = db.select(Collection).filter_by(collection_id=collection_id)
    collection = db.session.scalar(stmt)
    if collection:
        stmt = db.select(Game).filter_by(game_id=game_id)
        game = db.session.scalar(stmt)
        if game:
            return game_schema.dump(game)
        else:
            return {'error': f'Game {game.title} could not be found'}, 404

# add a single game into a collection
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

# This route and method will delete a game from a collection
@games_bp.route('/<int:game_id>', methods=['DELETE'])
def delete_game(collection_id, game_id):
    stmt = db.select(Collection).filter_by(collection_id=collection_id)
    collection = db.session.scalar(stmt)
    if collection:
        stmt = db.select(Game).filter_by(game_id=game_id)
        game = db.session.scalar(stmt)
        if game:
            db.session.delete(game)
            db.session.commit()
            return {'message': f'Game -{game.title}- has been successfully deleted'}
        else:
            return {'error': f'Game -{game.title}- could not be found'}, 404

# To update the information in the Game model, change records within the table.
@games_bp.route('/<int:game_id>', methods=['PUT', 'PATCH'])
def update_game(collection_id, game_id):
    stmt = db.select(Collection).filter_by(collection_id=collection_id)
    collection = db.session.scalar(stmt)
    if collection:
        body_data = game_schema.load(request.get_json(), partial=True)
        stmt = db.select(Game).filter_by(game_id=game_id)
        game = db.session.scalar(stmt)
        if game:
            game.title = body_data.get('title')
            game.platform = body_data.get('platform')
            game.genre = body_data.get('genre')
            game.multiplayer = body_data.get('multiplayer') 
            game.release_date = body_data.get('release_date')
            game.edition = body_data.get('edition')
            db.session.commit()
            return game_schema.dump(game)
        else:
            return {'error': f'Game -{game.title}- could not be found'}, 404