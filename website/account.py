from flask import Blueprint, render_template, request
from .models import User
from flask_login import login_required, current_user
from . import db

account = Blueprint('account', __name__)

@account.route('/top-account', methods=['GET','POST'])
@login_required
def top_account():
    if request.method == 'POST':
        user = User.query.filter_by(email=current_user.email).first() # type: ignore
        amount = request.form.get('top_amount')
        try:
            if user.balance:
                user.balance = int(user.balance) + int(amount)
            else:
                user.balance = 0
            db.session.commit()
        except TypeError:
            print("Error at account topping")
    return render_template("account.html", user=current_user)


@account.route('/account', methods=['GET','POST'])
@login_required
def account_view():
    return render_template("account.html", user=current_user)
