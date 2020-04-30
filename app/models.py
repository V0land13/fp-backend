from app import db
from flask_security import RoleMixin, UserMixin

######### Users & Roles
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    active = db.Column(db.Boolean())
    questions = db.relationship('Question', backref='question_manager', lazy='dynamic')
    qlists = db.relationship('QuestionList', backref='questionlist_manager', lazy='dynamic')

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

questionlists = db.Table('questionlists',
    db.Column('questionlist_id', db.Integer(), db.ForeignKey('question_list.id')),
    db.Column('question_id', db.Integer(), db.ForeignKey('question.id'))
)

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



