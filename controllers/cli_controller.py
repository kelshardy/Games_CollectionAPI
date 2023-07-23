from init import db, bcrypt
from models.user import User
from models.collection import Collection
from models.game import Game
from models.review import Review
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
        ),
        User(
            name='User 2',
            email="user2@email.com",
            password=bcrypt.generate_password_hash('user2pw').decode('utf-8')
        )
    ]
    
    db.session.add_all(users)
    
    collections = [
        Collection(
            label='My Collection',
            user=users[0]
        )
    ]
    
    db.session.add_all(collections)
    
    games = [
        Game(
            title='The Last Of Us',
            platform='PS5',
            genre='Survival Horror',
            multiplayer='No',
            release_date='02-09-2022'
        )
    ]
    
    db.session.add_all(games)
    
    db.session.commit()
    
    print("Tables Seeded")