from flask import Flask, request, render_template, redirect
from dbbase import ControlBD


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'


@app.route('/', methods=['GET'])
def index():
    groceries = contr.get()
    return render_template('index.html', groceries=groceries, info='')

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
        patient.count = int(eval(request.form['count']))
        patient.price = int(request.form['price'])
        return redirect('/')
    return render_template('edit.html', product=patient)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    contr.del_position(id=id)
    return redirect('/')

@app.route('/edit_count/<int:id>&<int:dop>', methods=['GET', 'POST'])
def edit_count(id, dop):
    product = contr.find(id=id)
    product.count += dop - 1
    contr.commit()
    return redirect('/')
@app.route('/find/', methods=['GET', 'POST'])
def find():
    print(request.form['k_find'], request.form['i_find'])
    groceries = contr.get()
    yes = []
    fi = request.form['i_find']
    info = 'Нет информации'
    for i in groceries:
        if request.form['k_find'] == 'id' and fi in str(i.id):
            yes.append(i)
            info = 'Артикулу со значением '+ fi
        elif request.form['k_find'] == 'name' and fi in str(i.name):
            yes.append(i)
            info = 'Названию со значением '+ fi
        elif request.form['k_find'] == 'dep' and fi in str(i.description):
            yes.append(i)
            info = 'Описанию со значением '+ fi
        elif request.form['k_find'] == 'count' and fi in str(i.count):
            yes.append(i)
            info = 'Количеству со значением '+ fi
        elif request.form['k_find'] == 'prise' and fi in str(i.price):
            yes.append(i)
            info = 'Цене со значением '+ fi
    return render_template('index.html', groceries=yes, info=info)

if __name__ == '__main__':
    contr = ControlBD()
    app.run(debug=True)