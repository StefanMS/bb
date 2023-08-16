from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect
import os
from werkzeug.utils import secure_filename
from .models import Collection, User, Bidding_Basket
from . import db

admin = Blueprint('admin', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower in ALLOWED_EXTENSIONS


@admin.route('/add-game', methods=['GET','POST'])
@login_required
def add_game():
    if request.method == 'POST':

        # image handling
        print(request.files)
        if 'img' not in request.files:
            flash('No file detected')
            return redirect('/admin', code=302)
        file = request.files['img']
        if file.filename == '':
            flash('Invalid file name')
            return redirect('/admin', code=302)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) # type: ignore
            file.save(os.path.join('', filename))

        # game details handiling
        game_name = request.form.get('game_name')
        
        game_status = 'active' if request.form.get('active_game') \
                        else 'inactive'
        #game_status = request.form.get('activate_game')

        new_game = Collection(game_name=game_name, game_status = game_status)
        db.session.add(new_game)
        db.session.commit()
        flash('Game added!', category='Success')

    return redirect('/admin', code=302)


@admin.route('/activate-game', methods=['GET','POST'])
@login_required
def activate_game():

    if request.method == 'POST':
        try:
            game_id = request.args.get('gameid')
            collection = Collection.query.filter_by(game_id=game_id).first()
            collection.game_status = "active" \
                if collection.game_status == "inactive" \
                    else "inactive"
            db.session.commit()
            flash('Change successful!', category="success")
   
        except:
            print("Activation error")
    return redirect('/admin', code=302)


@admin.route('/reset-game', methods=['GET','POST'])
@login_required
def reset_game():

    if request.method == 'POST':
        try:
            game_id = request.args.get('gameid')
            Bidding_Basket.query.filter_by(game_id=game_id).delete()
            db.session.commit()
            flash('Reset successful!', category="success")

        except:
            print("Activation error")
    return redirect('/admin', code=302)


@admin.route('/admin', methods=['GET','POST'])
@login_required
def admin_view():
    collection = Collection.query
    users = User.query
    return render_template("admin.html", user=current_user, collection=collection, users=users)
