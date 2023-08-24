from main import *
@app.route('/product/', methods=['GET'])
def product():
    if log_question():
        groceries = contr.get_product()
        return render_template('product/index.html', groceries=groceries, info='', choise='product')
    else:
        return render_template('regandlog/log.html')

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if not log_question():
        return render_template('regandlog/log.html')
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        weight = request.form['quantity']
        price = request.form['price']
        contr.add_product(name, int(price), description=desc, count=int(weight))
        return redirect('/product/')
    return render_template('product/add_product.html', choise='product')

@app.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if not log_question():
        return render_template('regandlog/log.html')
    patient = contr.find_product(id=id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.description = request.form['description']
        patient.count = int(eval(request.form['count']))
        patient.price = int(request.form['price'])
        contr.commit()
        return redirect('/product/')
    return render_template('product/edit_product.html', product=patient, choise='product')


@app.route('/product/delete/<int:id>', methods=['POST'])
def delete_product(id):
    if not log_question():
        return render_template('regandlog/log.html')
    contr.del_product(id=id)
    return redirect('/product/')


@app.route('/product/edit_count/<int:id>&<int:dop>', methods=['GET', 'POST'])
def edit_count(id, dop):
    if not log_question():
        return render_template('regandlog/log.html')
    product = contr.find_product(id=id)
    product.count += dop - 1
    contr.commit()
    return redirect('/product')


@app.route('/product/find/', methods=['GET', 'POST'])
def product_find():
    if not log_question():
        return render_template('regandlog/log.html')
    groceries = contr.get_product()
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
    return render_template('product/index.html', groceries=yes, info=info, choise='product')