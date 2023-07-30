from init import db
from flask import Blueprint, request
from models.user import User
from models.collection import Collection, collection_schema, collections_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from .game_controller import games_bp

collections_bp = Blueprint('collections', __name__, url_prefix='/collections')
collections_bp.register_blueprint(games_bp, url_prefix='/<int:collection_id>/games')

# function to view all collections
@collections_bp.route('/')
@jwt_required()
def get_collection():
    stmt = db.select(Collection)
    collections = db.session.scalars(stmt)
    return collections_schema.dump(collections)

# function to view one collection
@collections_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_one_collection(id):
    stmt = db.select(Collection).filter_by(collection_id=id)
    collection = db.session.scalar(stmt)
    return collection_schema.dump(collection)

# function to create a collection
@collections_bp.route('/', methods=['POST'])
@jwt_required()
def create_collection():
    body_data = collection_schema.load(request.get_json())
    collection = Collection(
        label=body_data.get('label'),
        user_id=get_jwt_identity()       
    )
    db.session.add(collection)
    db.session.commit()
    return collection_schema.dump(collection), 201

# function to delete an individual collection    
@collections_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_collection(id):
    stmt = db.select(Collection).filter_by(collection_id=id)
    collection = db.session.scalar(stmt)
    if collection:
        db.session.delete(collection)
        db.session.commit()
        return {'message': f'Collection {collection.label}- deleted'}
    else:
        return {'error': f'No collection if -{collection.label}- found'}, 404
    
# function to update/change the collection's header
@collections_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_collection(id):
    body_data = collection_schema.load(request.get_json(), partial=True)
    stmt = db.select(Collection).filter_by(collection_id=id)
    collection = db.session.scalar(stmt)
    if collection:
        collection.label = body_data.get('label')
        db.session.commit()
        return collection_schema.dump(collection)
    else:
        return {'error': f'No collection with {collection.label} found'}, 404