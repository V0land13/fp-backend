from app import app, db
from flask import jsonify, render_template, flash, redirect, url_for, request, Markup
from flask_security import current_user, roles_required
from flask_security.utils import hash_password
from werkzeug.urls import url_parse
from .models import User, Role, Question, Answer
from .forms import QuestionAddForm, QuestionEditForm

@app.route('/manager')
@roles_required('manager')
def manager_view():
    return jsonify('manager cabinet')

# Страницы на встроенном шаблонизаторе
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
        flash('Вопрос не найден:')
        return redirect(url_for('manage_questions'))



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
        return jsonify({'ststus': True, 'error': 'Вопрос удален'})
    except:
        return jsonify({'ststus': False, 'error': 'Вопрос не найден'})
