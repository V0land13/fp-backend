from app import db
from flask_security import RoleMixin, UserMixin
from datetime import datetime

######### Association tables
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

questionlists = db.Table('questionlists',
    db.Column('questionlist_id', db.Integer(), db.ForeignKey('question_list.id')),
    db.Column('question_id', db.Integer(), db.ForeignKey('question.id'))
)

questionlistsdone = db.Table('questionlistsdone',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('questionlist_id', db.Integer, db.ForeignKey('question_list.id'))
)


######### Users & Roles

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    active = db.Column(db.Boolean())
    # manager communications
    questions = db.relationship('Question', backref='question_manager', lazy='dynamic')
    qlists = db.relationship('QuestionList', backref='questionlist_manager', lazy='dynamic') #листы менеджера
    # users results data
    completed_question_lists = db.relationship('QuestionList', secondary=questionlistsdone, backref=db.backref('completed_users', lazy='dynamic'))


    def __repr__(self):
        return '<User {}>'.format(self.email)

    def is_user_question(self, checked_id):
        for q in self.questions.all():
            if q.q_id==checked_id:
                return True
        return False


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(255))

######### Questions & QueslionList

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    manager = db.Column(db.Integer, db.ForeignKey('user.id'))
    single_answer = db.Column(db.Boolean)
    img = db.Column(db.String(120), nullable=True)
    answers = db.relationship('Answer', backref='question_for', lazy='dynamic')


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    question = db.Column(db.Integer, db.ForeignKey('question.id'))

class QuestionList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    manager = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_on = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Вопросы
    questions = db.relationship('Question',
                               secondary=questionlists,
                               backref=db.backref('questionlists', lazy='dynamic'),
                               lazy='dynamic')

    def q_add(self, question):
        if not self.is_added(question):
            self.questions.append(question)
            return self

    def q_remoove(self, question):
        if self.is_added(question):
            self.questions.remove(question)
            return self

    def is_added(self, question):
        return self.questions.filter(questionlists.c.question_id == question.id).count()

    def all_questions(self):
        return Question.query.join(questionlists, (questionlists.c.question_id == Question.id)).filter(questionlists.c.questions_list_id == self.id)

class QuestionInList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_list = db.Column(db.Integer, db.ForeignKey('question_list.id'))
    question = db.Column(db.Integer, db.ForeignKey('question.id'))
    rate = db.Column('Балы за вопрос', db.Integer)
    response_waiting_time = db.Column('Время на ответ в минутах', db.Integer)
    __table_args__ = (db.UniqueConstraint('question_list', 'question', name='_question_list_question_uc'),)

### Users results

class UserAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    q_in_l = db.Column(db.Integer, db.ForeignKey('question_in_list.id'))
    q_start_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_success = db.Column(db.Boolean(), nullable=True)
