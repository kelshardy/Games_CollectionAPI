from init import db, bcrypt
from flask_jwt_extended import create_access_token
from flask import Blueprint, request
from models.user import User, user_schema, users_schema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta
from .collection_controller import collections_bp

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_bp.register_blueprint(collections_bp, url_prefix='/<int:user_id>/collections')

# Creates a User login for use within the application by collecting a name, email and password from the user
@auth_bp.route('/register', methods=['POST'])
def auth_register():
    try:
        body_data = request.get_json()
        user = User()
        user.name = body_data.get('name')
        user.email = body_data.get('email')
        if body_data.get('password'):
            user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        db.session.add(user)
        db.session.commit()
        # Adds the User into the system
        return user_schema.dump(user), 201
    except IntegrityError as err:
        # If the email is already registered it will throw an error
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return { 'error': 'Email address already in use' }, 409
        # An error is thrown if information is missing from the registration
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return { 'error': f'The {err.orig.diag.column_name} is required' }, 409

# Route allows User to login    
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    body_data = request.get_json()
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)
    # If the login information is correct, a token will generate for User access
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(days=1))
        return { 'email':user.email, 'token': token }
    # If information provided is incorrect, will throw error
    else:
        return { 'error': 'Invalid email or password' }, 401