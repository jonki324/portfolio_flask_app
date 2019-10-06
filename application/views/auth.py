from flask import Blueprint, render_template

auth_view = Blueprint('auth_view', __name__)


@auth_view.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@auth_view.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')
