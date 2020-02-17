from flask import render_template, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flasklogin import app, db
from flasklogin.forms import RegisterForm, LoginForm
from flasklogin.models import Admin

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Admin(name=form.name.data, email=form.email.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data} sucessfully!!', 'sucess')
        return redirect('/login')
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Welcome {form.name.data}')
        return redirect('/home')
    return render_template('login.html', form=form)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
