from main import *
@app.route('/prise/find/', methods=['GET', 'POST'])
def prise_find():
    if not log_question():
        return render_template('regandlog/log.html')
    groceries = contr.get_prise()
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
        elif request.form['k_find'] == 'prise' and fi in str(i.price):
            yes.append(i)
            info = 'Поиск по цене со значением ' + fi
    return render_template('prise/prise.html', groceries=yes, info=info, choise='prise')

@app.route('/prise/edit/<int:id>', methods=['GET', 'POST'])
def edit_prise(id):
    if not log_question():
        return render_template('regandlog/log.html')
    patient = contr.find_prise(id=id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.description = request.form['description']
        patient.price = int(request.form['price'])
        contr.commit()
        return redirect('/prise')
    return render_template('prise/edit_prise.html', product=patient, choise='prise')


@app.route('/prise/delete/<int:id>', methods=['POST'])
def delete_prise(id):
    if not log_question():
        return render_template('regandlog/log.html')
    contr.del_prise(id=id)
    return redirect('/prise')


@app.route('/prise/', methods=['GET'])
def ind_prise():
    if log_question():
        groceries = contr.get_prise()
        return render_template('prise/prise.html', groceries=groceries, info='', choise='prise')
    else:
        return render_template('regandlog/log.html')


@app.route('/prise/add', methods=['GET', 'POST'])
def add_prise():
    if not log_question():
        return render_template('log.html')
    if request.method == 'POST':
        print(request.form)
        if 'box' in request.form.keys():
            rec = []
            print(request.form)
            for i in range(1, app.bibl[str(current_user.username) + 'rec'] + 1):
                rec.append(app.bibl[str(current_user.username) + str(i)])
            contr.add_position(name=app.bibl[str(current_user.username) + 'name'],
                               price=app.bibl[str(current_user.username) + 'prise'],
                               recept=(' '.join(rec)).replace('_', ' '), description=app.bibl[str(current_user.username) + 'des'])
            return redirect('/prise')
        else:
            rec = []
            if 'k_find' in request.form.keys():
                app.bibl[str(current_user.username) + 'rec'] += 1
                app.bibl[str(current_user.username) + str(app.bibl[str(current_user.username) + 'rec'])] = request.form[
                                                                                                               'k_find'] + ' ' + \
                                                                                                           request.form[
                                                                                                               'number']
                for i in range(1, app.bibl[str(current_user.username) + 'rec'] + 1):
                    rec.append(app.bibl[str(current_user.username) + str(i)])
            else:
                app.bibl[str(current_user.username) + 'name'] = request.form['name']
                app.bibl[str(current_user.username) + 'des'] = request.form['des']
                app.bibl[str(current_user.username) + 'prise'] = request.form['prise']
            return render_template('prise/add2.html', groceries=contr.get_product(), rec=rec, choise='prise')
    app.bibl[str(current_user.username) + 'rec'] = 0
    return render_template('prise/add_prise.html', groceries=contr.get_product(), choise='prise')
