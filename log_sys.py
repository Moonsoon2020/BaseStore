from main import *

@login_manager.user_loader
def load_user(user_id):
    return contr.load_user(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if log_question():
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = contr.user_get_p(username)
        if user and check_password_hash(user.password, password) and user.ok:
            login_user(user)
            current_user.username = username
            current_user.password = password
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('regandlog/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return render_template('regandlog/log.html')
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
    return render_template('regandlog/register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))