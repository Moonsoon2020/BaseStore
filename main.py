from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from dbbase import ControlBD

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.bibl = {}
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

@app.route('/', methods=['GET'])
def index():
    if log_question():
        groceries = contr.get_product()
        return render_template('index.html', groceries=groceries, info='', choise='product')
    else:
        return render_template('regandlog/log.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if not log_question():
        return render_template('regandlog/log.html')
    if request.method == 'POST':
        return redirect('/')
    return render_template('settings.html')

