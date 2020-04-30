from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import validators
from app.models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Пароль', validators=[validators.DataRequired()])
    password2 = PasswordField(
        'Подтвердите пароль', validators=[validators.DataRequired(), validators.EqualTo('password')])
    first_name = StringField('Имя', validators=[validators.DataRequired()])
    last_name = StringField('Фамилия', validators=[validators.DataRequired()])
    submit = SubmitField('Зарегистрироваться')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
        
class QuestionAddForm(FlaskForm):
    question = StringField('Вопрос', validators=[validators.DataRequired()])
    single_answer = BooleanField('Возможно выбрать только 1 ответ?')
    answer1 = StringField('Ответ 1', validators=[validators.DataRequired()])
    answer2 = StringField('Ответ 2', validators=[validators.DataRequired()])
    answer3 = StringField('Ответ 3', validators=[validators.DataRequired()])
    answer4 = StringField('Ответ 4', validators=[validators.DataRequired()])
    submit = SubmitField('Создать вопрос')

class QuestionEditForm(QuestionAddForm):
    submit = SubmitField('Сохранить изменения')