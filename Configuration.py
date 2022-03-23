from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import  Mail ,Message


app = Flask(__name__)


app.config['SECRET_KEY'] = 'mypowerofhellfire'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users_List.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'zayniddinm956@gmail.com'
app.config['MAIL_PASSWORD'] = 'occufzywtfzvrlfh'
app.config['MAIL_DEFAULT_SENDER'] = 'zayniddinm834@gmail.com'

mess = Mail(app)
db = SQLAlchemy(app)
