from flask import Blueprint, render_template, request, flash, jsonify, redirect
from .models import Note, User, Collection
from flask_login import login_required, current_user
from . import db
import json

admin = Blueprint('admin', __name__)

@admin.route('/add-game', methods=['GET','POST'])
@login_required
def add_game():
    if request.method == 'POST':
        game_name = request.form.get('game_name')
        game_status = request.form.get('game_status')
        try:
            new_game = Collection(game_name=game_name, game_status = game_status)
            db.session.add(new_game)
            db.session.commit()
            flash('Game added!', category='Success')
        except:
            pass
    return redirect('/admin', code=302)

@admin.route('/activate-game', methods=['GET','POST'])
@login_required
def activate_game():
    
    user = User.query.filter_by(email=current_user.email).first()

    if request.method == 'POST':
        try:
            game_id = request.args.get('gameid')
            collection = Collection.query.filter_by(game_id=game_id).first()
            collection.game_status = "active" if collection.game_status == "inactive" else "inactive"
            db.session.commit()
            flash('Change successful!', category="success")
                
        except:
            print("Activation error")
    return redirect('/admin', code=302)

@admin.route('/admin', methods=['GET','POST'])
@login_required
def admin_view():
    collection = Collection.query
    
    return render_template("admin.html", user=current_user, collection=collection)

