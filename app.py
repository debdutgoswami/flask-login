from flask import Flask, render_template, redirect, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, RecaptchaField, CSRFProtect
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager

app = Flask(__name__)
csrf = CSRFProtect(app)
#loginmanager = LoginManager(app)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.db'
#app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeiXNkUAAAAAJ3XH5xSYRXOf1oK2KQwDWkeDgQg'
Bootstrap(app)
db = SQLAlchemy(app)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(180))

class LoginForm(FlaskForm):
    email = StringField('username', validators=[InputRequired(), Length(max=50), Email(message='Invalid Email')], id='email')
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)], id='psd')
    remember = BooleanField('remember me')
    #recaptcha = RecaptchaField()

class RegisterForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(min=4, max=50)], id='name')
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)], id='email')
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)], id='psd')
    confirm_password = PasswordField('confirm password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('password', message="Paswords should match")], id='cnfpsd')
    #recaptcha = RecaptchaField()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Admin(name=form.name.data, email=form.email.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data} sucessfully!!')
        return redirect('/login')
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    return render_template('login.html', form=form)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    csrf.init_app(app)
    #loginmanager.init_app(app)
    app.run(host='0.0.0.0', port=8080, debug=True)