# "." inseamna ca face import din aplicatia curenta (from this package). 
# echivalent cu "from website import db" daca am fi in afara folderului
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default= func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    # last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    balance = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), default= func.now())
    notes = db.relationship('Note')

# All games
class Collection(db.Model):
    game_id = db.Column(db.Integer, primary_key=True) 
    game_name = db.Column(db.String(150))
    #game_countdown = db.Column(db.DateTime(timezone=True), default= func.now()) # placeholder
    game_status = db.Column(db.String(150))
    #game_status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), default= func.now())

# All bids
class Bidding_Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('collection.game_id'))
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #game_status = db.Column(db.Boolean)
