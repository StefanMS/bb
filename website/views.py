'''
Home page backend
'''
from datetime import datetime, timedelta
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect, jsonify
import logging
from .models import User, Collection, Bidding_Basket

from . import db

logging.basicConfig(level=logging.INFO, filename="logs/app_logs.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

views = Blueprint('views', __name__)


@views.route('/', methods=['GET','POST'])
@login_required
def home():
    '''
    Home route with user-filtered collection
    '''
    active_games = Collection.query.filter_by(game_status="active")
    games_json = jsonify_collection(active_games)

    return render_template("home.html", user=current_user, games_json=games_json)


@views.route('/bid', methods=['GET','POST'])
@login_required
def bid():
    '''
    Enlisting function for each game
    '''
    user = User.query.filter_by(email=current_user.email).first() # type: ignore

    if request.method == 'POST':

        game_id = request.args.get('gameid')
        if int(user.balance) > 0:
            user.balance = int(user.balance) - 1
            new_bid = Bidding_Basket(game_id=game_id, player_id=user.id)
            db.session.add(new_bid)
            db.session.commit()
            logging.info("User: # %s enrolled for game: # %s ", user.id, game_id)
            flash('Enrolling successful!', category="success")

    return redirect('/', code=302)

@views.route('/api/collection', methods=['GET'])
def collection_api():
    '''
    API to view all games
    '''
    collection = Collection.query
    games_json = []
    for game in collection:
        game_as_dict = {
            'id' : game.game_id,
            'name' : game.game_name,
            'status' : game.game_status,
        }
        games_json.append(game_as_dict)
    return jsonify(games_json)

# IT DOES NOT SEND A JSON, BUT A LIST!
def jsonify_collection(active_games) -> list:
    '''
        The function takes a user-filtered query, not intended for whole collection
    '''
    games_json = []
    for game in active_games:
        bidding_basket = Bidding_Basket.query.filter_by(game_id=game.game_id)
        game_capacity = bidding_basket.count()
        enrolled_user_bool = True if Bidding_Basket.query.filter_by(\
            game_id=game.game_id, player_id=current_user.id).first() \
            else False
        now_timestamp = datetime.now().timestamp()
        countdown = now_timestamp - game.created_at.timestamp()
        #print(timedelta(seconds=countdown))
        game_as_dict = {
            'id' : game.game_id,
            'name' : game.game_name,
            'status' : game.game_status,
            'enrolled_user' : enrolled_user_bool,
            'capacity' : game_capacity,
            'countdown' : str(f'{int(countdown//3600)} hours left')
        }
        games_json.append(game_as_dict)
    return games_json
