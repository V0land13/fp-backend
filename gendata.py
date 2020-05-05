import random, sys
from app import app, db
from flask_security.utils import hash_password
from app.models import User, Role, Question, Answer
from app.security import user_datastore


def role_gen():
    #Генерация ролей
    user_datastore.create_role(name='admin', description='Administrator')
    user_datastore.create_role(name='manager', description='can manage questions and question lists')
    user_datastore.create_role(name='user', description='basic role')
    db.session.commit()
    print('Roles generation done')

def add_roles_to_user(user_id):
    user = User.query.get(user_id)
    user_datastore.add_role_to_user(user, Role.query.filter(Role.name == 'admin').first())
    user_datastore.add_role_to_user(user, Role.query.filter(Role.name == 'manager').first())
    db.session.commit()
    print('Roles was add')

def question_generator(manager_id, number):
    # Генерация вопросов
    n = int(number)
    id = int(manager_id)
    for i in range(0, n):
        print(i)
        new_question = Question(text='Question {}'.format(i), manager=id, single_answer=random.choice([True, False]))
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
    print('questions was generated')

def help():
    print('Заполнение базы первичными данными.')
    print('usage: python gendata.py [option args]')
    print('    rolesgen             - без аргументов, добавляет в таблицу роли админа, менеджера и юзера')
    print('    roles-to-user id     - аргумент id пользователя, добавит ему роль менеджера и админа')
    print('    qgen id num          - сгенерирует менеджеру с id вопросы в колличестве num')
    print('    help                 - эта справка')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('Внимание чтобы добавить роль пользователю создайте его!')


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == 'help':
        help()
    elif sys.argv[1] == 'rolesgen':
        role_gen()
    elif sys.argv[1] == 'roles-to-user':
        add_roles_to_user(sys.argv[2])
    elif sys.argv[1] == 'qgen':
        question_generator(sys.argv[2], sys.argv[3])