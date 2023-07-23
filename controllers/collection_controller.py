from init import db
from flask import Blueprint, request
from models.user import User
from models.collection import Collection, collection_schema, collections_schema
from flask_jwt_extended import jwt_required

collections_bp = Blueprint('collections', __name__, url_prefix='/collections')

@collections_bp.route('/')
def get_collection():
    stmt = db.select(Collection)
    collections = db.session.scalars(stmt)
    return collections_schema.dump(collections)

@collections_bp.route('/', methods=['POST'])
@jwt_required()
def create_collection():
    body_data = collection_schema.load(request.get_json())
    collection = Collection(
        label=body_data.get('label'),
        user_id=body_data.get('user_id'),
        game_id=body_data.get('game_id')         
    )
    db.session.add(collection)
    db.session.commit()
    return collection_schema.dump(collection), 201

@collections_bp.route('/', methods=['DELETE'])
@jwt_required()
def delete_collection():
    stmt = db.select(Collection)
    collection = db.session.scalar(stmt)
    if collection:
        db.session.delete(collection)
        db.session.commit()
        return {'message': f'Collection {collection.id} deleted successfully'}
    else:
        return {'error': f'Collection {collection.id} not found'}, 404