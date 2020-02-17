from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
loginmanager = LoginManager(app)
loginmanager.login_view = 'login'
loginmanager.login_message_category = 'info'
app.config['SECRET_KEY'] = '02d3bdfdd92f6fe0ee9c5ba14e66e314'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.db'

from flasklogin import routes
