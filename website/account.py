from flask import Blueprint, render_template, request
from .models import User
from flask_login import login_required, current_user
import logging
from . import db

logging.basicConfig(level=logging.INFO, filename="logs/app_logs.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

account = Blueprint('account', __name__)

@account.route('/top-account', methods=['GET','POST'])
@login_required
def top_account():
    if request.method == 'POST':
        user = User.query.filter_by(email=current_user.email).first() # type: ignore
        amount = request.form.get('top_amount')
        try:
            if user.balance:
                user.balance = int(user.balance) + int(amount) # type: ignore
                logging.info("User: # %s added %s coins", user.id, amount)
            else:
                user.balance = 0
                logging.info("User: # %s set to 0 coins", user.id)
            db.session.commit()
        except TypeError:
            logging.info("User: #  %s failed to top-up", user.id)
    return render_template("account.html", user=current_user)


@account.route('/account', methods=['GET','POST'])
@login_required
def account_view():
    return render_template("account.html", user=current_user)
