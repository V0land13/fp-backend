from app import app, db
from flask import jsonify, render_template, flash, redirect, url_for, request, Markup
from flask_security import current_user, roles_required
from flask_security.utils import hash_password
from werkzeug.urls import url_parse

from datetime import datetime, timedelta

from .models import User, Role, Question, Answer, QuestionList, QuestionInList
from .forms import QuestionAddForm, QuestionEditForm


# Страницы на встроенном шаблонизаторе
@app.route('/manager')
@app.route('/manager/questions')
@roles_required('manager')
def manage_questions():
    user = '{} {}'.format(current_user.first_name, current_user.last_name)
    questions = Question.query.all()
    return render_template('manager_questions.html', user = user, questions= questions)

@app.route('/manager/add-question', methods=['GET', 'POST'])
@roles_required('manager')
def question_add_view():
    user = '{} {}'.format(current_user.first_name, current_user.last_name)
    form = QuestionAddForm()
    if form.validate_on_submit():
        new_question=Question(text=form.question.data, manager=int(current_user.id), single_answer=form.single_answer.data)
        db.session.add(new_question)
        db.session.commit()
        new_q_id=new_question.id
        answer1=Answer(text=form.answer1.data, question=new_q_id)
        db.session.add(answer1)
        answer2 = Answer(text=form.answer2.data, question=new_q_id)
        db.session.add(answer2)
        answer3 = Answer(text=form.answer3.data, question=new_q_id)
        db.session.add(answer3)
        answer4 = Answer(text=form.answer4.data, question=new_q_id)
        db.session.add(answer4)
        db.session.commit()
        flash('Вопрос успешно добавлен')
        return redirect(url_for('manage_questions'))
    return render_template('question-add.html', user = user, form = form)

@app.route('/manager/dell_question/<q_id>', methods=['GET', 'POST'])
@roles_required('manager')
def dell_question(q_id):
    question = Question.query.get(q_id)
    try:
        db.session.delete(question)
        db.session.commit()
        flash(Markup('Удален вопрос: </br> {}'.format(question.text)))
        return redirect(url_for('manage_questions'))
    except:
        flash('Вопрос не найден:')
        return redirect(url_for('manage_questions'))

@app.route('/manager/edit_question/<q_id>', methods=['GET', 'POST'])
@roles_required('manager')
def edit_question(q_id):
    user = '{} {}'.format(current_user.first_name, current_user.last_name)
    question = Question.query.get(q_id)
    try:
        form = QuestionEditForm()
        if form.validate_on_submit():
            question.text = form.question.data
            question.single_answer = form.single_answer.data
            question.answers[0].text=form.answer1.data
            question.answers[1].text=form.answer2.data
            question.answers[2].text=form.answer3.data
            question.answers[3].text=form.answer4.data
            db.session.commit()
            flash('Вопрос успешно изменен')
            return redirect(url_for('manage_questions'))

        elif request.method == 'GET':
            form.question.data = question.text
            form.single_answer.data = question.single_answer
            form.answer1.data = question.answers[0].text
            form.answer2.data = question.answers[1].text
            form.answer3.data = question.answers[2].text
            form.answer4.data = question.answers[3].text
        return render_template('question-edit.html', user=user, form=form)
    except:
        flash(u'Вопрос не найден', 'error')
        return redirect(url_for('manage_questions'))

## Question lists management
@app.route('/manager/qlists')
@roles_required('manager')
def question_lists_view():
    user = '{} {}'.format(current_user.first_name, current_user.last_name)
    qls = QuestionList.query.all()
    return render_template('question-lists.html', user = user, qls= qls)

@app.route('/add-qlist', methods=['GET', 'POST'])
@roles_required('manager')
def question_list_add():
    user = '{} {}'.format(current_user.first_name, current_user.last_name)

    questions = Question.query.all()
    if request.method == 'POST':
        get_data = request.form.to_dict()
        new_ql = QuestionList(
            name=get_data.pop('QLname'),
            description=get_data.pop('QLtext'),
            manager=int(current_user.id),
            start_date=datetime.strptime(get_data.pop('start_date'), '%Y-%m-%d'),
            end_date=datetime.strptime(get_data.pop('end_date'), '%Y-%m-%d')
        )
        db.session.add(new_ql)

        question_ids_in_list = []
        for key, value in get_data.items():
            if value == 'on':
                question_ids_in_list.append(int(key))

        for id in question_ids_in_list:
            q_in_l = QuestionInList(
                question_list = new_ql.id,
                question = id,
                rate = get_data.get('{}-rate'.format(id)),
                response_waiting_time = int(get_data.get('{}-time'.format(id)))
            )
            db.session.add(q_in_l)
            new_ql.questions.append(Question.query.get(id))

        db.session.commit()
        return redirect(url_for('question_lists_view'))

    return render_template('question-list-add.html', user = user, questions=questions)


@app.route('/manager/qlist/<id>')
@roles_required('manager')
def manage_qlist(id):
    user = '{} {}'.format(current_user.first_name, current_user.last_name)
    ql = QuestionList.query.get(id)
    try:
        ql.id
    except:
        flash('Опрос не найден')
        return redirect(url_for('question_lists_view'))
    return render_template('questionlist.html', user=user, ql=ql)

@app.route('/manager/dellete-ql/<id>')
@roles_required('manager')
def ql_dellete(id):
    ql = QuestionList.query.get(id)
    try:
        db.session.delete(ql)
        db.session.commit()
        flash(Markup('Удален опрос: </br> {}'.format(ql.name)))
        return redirect(url_for('question_lists_view'))
    except:
        flash('Oпрос не найден:')
        return redirect(url_for('question_lists_view'))



# API routers
@app.route('/api/manager/questions')
@roles_required('manager')
def api_manage_questions():
    user = '{} {}'.format(current_user.first_name, current_user.last_name)
    questions = []
    for q in Question.query.all():
        questions.append({ 'id': q.id, 'text': q.text, 'manager': q.manager })
    return jsonify({'user': user, 'questions': questions})

@app.route('/api/dell_question/<q_id>', methods=['GET', 'POST'])
@roles_required('manager')
def api_dell_question(q_id):
    question = Question.query.get(q_id)
    try:
        db.session.delete(question)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Вопрос удален'})
    except:
        return jsonify({'status': 'error', 'message': 'Вопрос не найден'})

@app.route('/api/manager/add-question', methods=['POST'])
@roles_required('manager')
def question_add_api():
    form = request.form
    user = '{} {}'.format(current_user.first_name, current_user.last_name)
    if 'question' and 'single_answer' and 'answer1' and 'answer2' and 'answer3' and 'answer4' in form.keys():
        new_question=Question(text=form.get('question'), manager=int(current_user.id), single_answer=form.get('single_answer'))
        db.session.add(new_question)
        db.session.commit()
        new_q_id=new_question.id

        answer1=Answer(text=form.get('answer1'), question=new_q_id)
        db.session.add(answer1)
        answer2 = Answer(text=form.get('answer2'), question=new_q_id)
        db.session.add(answer2)
        answer3 = Answer(text=form.get('answer3'), question=new_q_id)
        db.session.add(answer3)
        answer4 = Answer(text=form.get('answer4.data'), question=new_q_id)
        db.session.add(answer4)
        db.session.commit()
        message = 'Вопрос добавлен успешно'
        status = 'success'
    else:
        message = 'Wrong data'
        status = 'error'
    return jsonify({ 'status': status, 'user': user, 'message': message })