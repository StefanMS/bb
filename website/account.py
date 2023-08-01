from flask import Blueprint, render_template, request, flash, jsonify
from .models import Note, User, Collection
from flask_login import login_required, current_user
from . import db
import json

account = Blueprint('account', __name__)

@account.route('/top-account', methods=['GET','POST'])
@login_required
def top_account():
    if request.method == 'POST':
        user = User.query.filter_by(email=current_user.email).first() # type: ignore
        if user.balance:
            user.balance = int(user.balance) + 10
        else:
            user.balance = 100
        db.session.commit()
    return render_template("account.html", user=current_user)


@account.route('/account', methods=['GET','POST'])
@login_required
def account_view():
    return render_template("account.html", user=current_user)
