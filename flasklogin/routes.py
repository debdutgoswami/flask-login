from flask import render_template, redirect, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flasklogin import app, db
from flasklogin.forms import RegisterForm, LoginForm
from flasklogin.models import Admin
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # checking is the user is already authenticated or not
    if current_user.is_authenticated:
        return redirect('/home')
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
    if current_user.is_authenticated:
        return redirect('/home')
    form = LoginForm()
    # for redirecting it to the original route from where the request came from
    next_page = request.args.get('next')
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            print(next_page, request.args)
            if next_page:
                return redirect(next_page)
            else:
                return redirect('/home')
        else:
            flash('Login Unsuccessful. Check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/home')

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
