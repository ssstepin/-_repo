from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Okay, I pull up, hop out at the after party You and all your friends, yeah, they love to get naughty Sippin on that Henn, I know you love that Bacardi (Sonny Digital) 1942, I take you back in that Rari Okay, I pull up, hop out at the after party You and all your friends, yeah, they love to get naughty Sippin on that Henn, I know you love that Bacardi 1942, I take you back in that Rari'
db = SQLAlchemy(app)

login_manager = LoginManager(app)

from IVR_app import models, routes
from .models import Users


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter(Users.id == user_id).first()
