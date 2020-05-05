from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

from config import Config


### make flask app with config###
app = Flask(__name__)
app.config.from_object(Config)


### init and migrate db ###
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Mail config
mail = Mail(app)


from app import routes, models, admin, security, manager