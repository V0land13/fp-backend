from app import app, db
from flask import request, redirect, url_for
from flask_security import current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from .models import *

class AdminView(ModelView):
    def is_accessible(self):
        try:
            result = current_user.has_role('admin')
        except:
            result = False
        return result

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        try:
            result = current_user.has_role('admin')
        except:
            result = False
        return result

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))

class MyRoleAdmin(AdminView):
  excluded_list_columns = ('users',)


admin = Admin(app, 'FlaskApp', index_view=MyAdminIndexView(name='Admin'))
admin.add_view(AdminView(User, db.session))
admin.add_view(MyRoleAdmin(Role, db.session))
admin.add_view(AdminView(Question, db.session))
admin.add_view(AdminView(Answer, db.session))
admin.add_view(AdminView(QuestionList, db.session))
#admin.add_view(AdminView(QuestionInList, db.session))
admin.add_view(AdminView(UserAnswers, db.session))
