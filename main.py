from flask import Flask, request, render_template, redirect
from dbbase import ControlBD, Praise


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'


@app.route('/', methods=['GET'])
def index():
    groceries = contr.get()
    return render_template('index.html', groceries=groceries)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        weight = request.form['quantity']
        price = request.form['price']
        contr.add_position(name, int(price), description=desc, count=int(weight))
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    patient = contr.find(id=id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.description = request.form['description']
        patient.count = int(request.form['count'])
        patient.price = int(request.form['price'])
        return redirect('/')
    return render_template('edit.html', product=patient)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    contr.del_position(id)
    return redirect('/')

@app.route('/edit_count_add/<int:id>', methods=['POST'])
def edit_count_add(id):
    product = contr.find(id=id)
    product.count += 1
    contr.commit()
    return redirect('/')

@app.route('/edit_count_minus/<int:id>', methods=['POST'])
def edit_count_minus(id):
    product = contr.find(id=id)
    product.count -= 1
    contr.commit()
    return redirect('/')

if __name__ == '__main__':
    contr = ControlBD()
    app.run(debug=True)