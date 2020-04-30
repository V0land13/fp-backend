from flask_security import Security, SQLAlchemyUserDatastore
from app import app, db
from .models import Role, User

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)