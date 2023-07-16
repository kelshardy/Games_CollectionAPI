from init import db, bcrypt
from models.user import User
from flask import Blueprint

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables Created")
    
@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables Dropped")
    
@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            name='User 1',
            email="user1@email.com",
            password=bcrypt.generate_password_hash('user1pw').decode('utf-8')
        )
    ]
    
    db.session.add_all(users)
    db.session.commit()
    
    print("Tables Seeded")