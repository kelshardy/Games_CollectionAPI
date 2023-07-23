from init import db 
from flask import Blueprint, request
from models.game import Game, game_schema, games_schema 

games_bp = Blueprint('games', __name__, url_prefix='/games')

@games_bp.route('/')
def list_games():
    stmt = db.select(Game).order_by(Game.title.desc())
    games = db.session.scalars(stmt)
    return games_schema.dump(games)

@games_bp.route('/', methods=['POST'])
def add_game():
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