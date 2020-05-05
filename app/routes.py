from app import app, db
from flask import jsonify, render_template, flash, redirect, url_for, request
from flask_security import current_user, login_user, logout_user, login_required
from flask_security.utils import hash_password
from werkzeug.urls import url_parse
from .models import *
from .forms import RegistrationForm
from .security import user_datastore


#User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = user_datastore.create_user(email=form.email.data, first_name = form.first_name.data, last_name = form.last_name.data)
        user.password = hash_password(form.password.data)
        try:
            user_datastore.add_role_to_user(user, Role.query.filter(Role.name == 'user').first())
        except:
            flash('Непредвиденная ошибка, попробуйте позже или обратитесь в поддержку')
            return render_template('register.html', title='Register', form=form)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('security.login'))
    return render_template('register.html', title='Register', form=form)

########## User pages ############

@app.route('/')
@login_required
def home():
    return redirect(url_for('backoffice'))

@app.route('/user')
@login_required
def backoffice():
    user = '{} {}'.format(current_user.first_name, current_user.last_name)
    available_qls = QuestionList.query.filter(
        QuestionList.start_date <= datetime.utcnow(),
        QuestionList.end_date >= datetime.utcnow(),
    ).all()
    return render_template('backoffice.html', user=user, available_qls=available_qls)

@app.route('/user/<id>')
@login_required
def user(id):
    user = '{} {}'.format(current_user.first_name, current_user.last_name)
    this_user = User.query.filter_by(id=id).first_or_404()
    return render_template('user-profile.html', this_user=this_user, user=user)

@app.route('/user/stat')
@login_required
def user_stat():
    return redirect(url_for('backoffice'))

@app.route('/user/ql/<id>', methods=['GET', 'POST'])
@login_required
def user_ql_passing(id):
    user = '{} {}'.format(current_user.first_name, current_user.last_name)
    try:
        ql = QuestionList.query.get(id)
        ql.id
    except:
        flash(u'Опрос не найден', 'error')
        return redirect(url_for('backoffice'))

    if request.method == 'POST':
        get_data = request.form.to_dict()
        print(get_data)
        flash(u'<Опрос пройден>', 'success')
        return redirect(url_for('backoffice'))



    return render_template('ql-passing.html', user=user, ql=ql)







######### delete it for prod
@app.route('/stat')
def stat():
    user_roles = []
    try:
        user = '{} {}'.format(current_user.first_name, current_user.last_name)
        for ur in current_user.roles:
            user_roles.append(ur.name)
    except:
        user = 'Гость'
    users = []
    roles = []
    for u in User.query.all():
        users.append('{} {}'.format(u.first_name, u.last_name))
    for r in Role.query.all():
        roles.append('{} - {}'.format(r.name, r.description))
    return jsonify({'!user': user,'user_roles': user_roles, 'users': users, 'roles': roles,'SECURITY_REGISTERABLE': app.config.get('SECURITY_REGISTERABLE')})
