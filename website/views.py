from flask import Blueprint, render_template, request, flash, redirect
from .models import User, Collection, Bidding_Basket
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET','POST'])
@login_required
def home():
    active_games = Collection.query.filter_by(game_status="active")
    game_dict = {}
    for game in active_games:
        bidding_basket = Bidding_Basket.query.filter_by(game_id=game.game_id)

        game_capacity = bidding_basket.count()
        enrolled_user = "enrolled" if Bidding_Basket.query.filter_by(game_id=game.game_id, player_id=current_user.id).first() else "not enrolled"

        game_dict[game] = {enrolled_user : game_capacity}
        print(game_dict)

    return render_template("home.html", user=current_user, game_dict=game_dict)


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



# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()
    
#     return jsonify({})