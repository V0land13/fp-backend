from app import app, db
from flask import jsonify, render_template, flash, redirect, url_for, request
from flask_security import current_user, login_user, logout_user, login_required
from flask_security.utils import hash_password
from werkzeug.urls import url_parse
from .models import User, Role, Question, Answer
from .forms import RegistrationForm
from .security import user_datastore

###### Общие страницы без прав доступа ######
@app.route('/')
def home():
    try:
        user = '{} {}'.format(current_user.first_name, current_user.last_name)
    except:
        user = 'Гость'
    users = []
    roles = []
    for u in User.query.all():
        users.append('{} {}'.format(u.first_name, u.last_name))
    for r in Role.query.all():
        roles.append('{} - {}'.format(r.name, r.description))
    return jsonify({'!user': user, 'users': users, 'roles': roles,'SECURITY_REGISTERABLE': app.config.get('SECURITY_REGISTERABLE')})

@app.route('/test')
@login_required
def test():
    user = current_user
    user_roles = []
    for r in user.roles:
        user_roles.append(r.name)
    return jsonify({'user.email': user.email, 'user.password': user.password, 'user.roles': user_roles})

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

# Manager funtions



#################
@app.route('/123')
def p_123():
    #user = User.query.filter(User.email == 'umqambi@tuta.io').first()
    #print(user.email)
    #user_datastore.create_role(name='admin', description='Administrator')
    #user_datastore.create_role(name='manager', description='can manage questions and question lists')
    #user_datastore.create_role(name='user', description='basic role')
    #user_datastore.add_role_to_user(user, Role.query.filter(Role.name == 'admin').first())
    #user_datastore.add_role_to_user(user, Role.query.filter(Role.name == 'manager').first())
    #db.session.commit()
    return 'ok'

@app.route('/q-generate')
def q_gen():
    import random
    for i in range(0, 20):
        new_question = Question(text='Question {}'.format(i), manager=1, single_answer=random.choice([True, False]))
        db.session.add(new_question)
        db.session.commit()
        new_q_id = new_question.id
        answer1 = Answer(text='Answer 1 for Question {}'.format(i), question=new_q_id)
        db.session.add(answer1)
        answer2 = Answer(text='Answer 2 for Question {}'.format(i), question=new_q_id)
        db.session.add(answer2)
        answer3 = Answer(text='Answer 3 for Question {}'.format(i), question=new_q_id)
        db.session.add(answer3)
        answer4 = Answer(text='Answer 4 for Question {}'.format(i), question=new_q_id)
        db.session.add(answer4)
        db.session.commit()
    return redirect(url_for('manage_questions'))