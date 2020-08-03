from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
bootstrap = Bootstrap(app)

cfg = {
    'user': 'postgres',
    'dbname': 'postgres',
    'host': 'ispace_database',
    'port': '5432',
    'password': 'airbus87_'
}

db_url = f"postgresql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['dbname']}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'l6q3dm17_snwoman87_'

db = SQLAlchemy(app)

# blueprint for auth routes in this app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for main routes in this app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

login_manager = LoginManager()
login_manager.login_view = 'auth.login_page'
login_manager.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
