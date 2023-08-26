from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from dbbase import ControlBD
import logging

logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="a")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.bibl = {}
app.logger.setLevel('DEBUG')
contr = ControlBD()


def log_question():
    if current_user.is_authenticated:
        user = contr.user_get_p(current_user.username)
        if user and user.ok:
            print(3)
            return True
        print(1, user, user.ok)
        return False
    else:
        print(2)
        return False


@app.route('/<id>', methods=['GET'])
def index(id):
    if not log_question():
        return render_template('regandlog/log.html')

    if id == 'start':
        app.bibl['table' + str(current_user.username)] = []
    elif id == -2:
        pass
    else:
        app.bibl['table' + str(current_user.username)].append([id, 1])

        return render_template('order_table.html', choise='table', prise=contr.get_prise(),
                               zak=app.bibl['table' + str(current_user.username)])


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if not log_question():
        return render_template('regandlog/log.html')
    if request.method == 'POST':
        return redirect('/')
    return render_template('settings.html', choise='settings')
