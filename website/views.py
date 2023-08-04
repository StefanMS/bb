from flask import Blueprint, render_template, request, flash, redirect
from .models import User, Collection, Bidding_Basket
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET','POST'])
@login_required
def home():
    active_games = Collection.query.filter_by(game_status="active")
    games_json = jsonify_collection(active_games)

    return render_template("home.html", user=current_user, games_json=games_json)


@views.route('/bid', methods=['GET','POST'])
@login_required
def bid():
    user = User.query.filter_by(email=current_user.email).first() # type: ignore

    if request.method == 'POST':
        try:
            game_id = request.args.get('gameid')
            if int(user.balance) > 0:
                user.balance = int(user.balance) - 1
                new_bid = Bidding_Basket(game_id=game_id, player_id=user.id)
                db.session.add(new_bid)
                db.session.commit()
                flash('Bit successful!', category="success")

        except: 
            print("Balance error") 
    return redirect('/', code=302)

# IT DOES NOT SEND A JSON, BUT A LIST!
def jsonify_collection(active_games) -> list:
    '''
        The function takes a user-filtered query, not intended for whole collection
    '''
    games_json = []
    for game in active_games:
        bidding_basket = Bidding_Basket.query.filter_by(game_id=game.game_id)

        game_capacity = bidding_basket.count()
        enrolled_user_bool = True if Bidding_Basket.query.filter_by(game_id=game.game_id, player_id=current_user.id).first() \
            else False
        now_timestamp = datetime.now().timestamp()
        countdown = now_timestamp - game.created_at.timestamp()
        print(timedelta(seconds=countdown))
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
