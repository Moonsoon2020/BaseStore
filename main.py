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
@login_manager.user_loader
def load_user(user_id):
    return contr.load_user(user_id)
@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        groceries = contr.get()
        return render_template('index.html', groceries=groceries, info='')
    else:
        return render_template('log.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = contr.user_get_p(username)
        if user and check_password_hash(user.password, password) and user.ok:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return render_template('log.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = contr.user_get_p(username)
        if user:
            flash('Username already taken')
        else:
            hashed_password = generate_password_hash(password)
            contr.add_user(username, hashed_password)
            flash('Account created successfully')
            return redirect(url_for('login'))
    return render_template('register.html')

# @app.route('/profile')
# def profile():
#     if current_user.is_authenticated:
#         return render_template('profile.html', user=current_user)
#     else:
#         return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        weight = request.form['quantity']
        price = request.form['price']
        contr.add_product(name, int(price), description=desc, count=int(weight))
        return redirect('/')
    return render_template('add.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        weight = request.form['quantity']
        price = request.form['price']
        contr.add_product(name, int(price), description=desc, count=int(weight))
        return redirect('/')
    return render_template('settings.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    patient = contr.find_product(id=id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.description = request.form['description']
        patient.count = int(eval(request.form['count']))
        patient.price = int(request.form['price'])
        return redirect('/')
    return render_template('edit.html', product=patient)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    contr.del_product(id=id)
    return redirect('/')


@app.route('/edit_count/<int:id>&<int:dop>', methods=['GET', 'POST'])
def edit_count(id, dop):
    product = contr.find_product(id=id)
    product.count += dop - 1
    contr.commit()
    return redirect('/')


@app.route('/find/', methods=['GET', 'POST'])
def find():
    groceries = contr.get()
    yes = []
    fi = request.form['i_find']
    info = 'Нет информации'
    for i in groceries:
        if request.form['k_find'] == 'id' and fi in str(i.id):
            yes.append(i)
            info = 'Поиск по артикулу со значением ' + fi
        elif request.form['k_find'] == 'name' and fi in str(i.name):
            yes.append(i)
            info = 'Поиск по названию со значением ' + fi
        elif request.form['k_find'] == 'dep' and fi in str(i.description):
            yes.append(i)
            info = 'Поиск по описанию со значением ' + fi
        elif request.form['k_find'] == 'count' and fi in str(i.count):
            yes.append(i)
            info = 'Поиск по количеству со значением ' + fi
        elif request.form['k_find'] == 'prise' and fi in str(i.price):
            yes.append(i)
            info = 'Поиск по цене со значением ' + fi
    return render_template('index.html', groceries=yes, info=info)



if __name__ == '__main__':
    contr = ControlBD()
    app.run(debug=True)
