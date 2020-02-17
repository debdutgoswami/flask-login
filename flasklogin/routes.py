import secrets, os
from PIL import Image
from flask import render_template, redirect, flash, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flasklogin import app, db
from flasklogin.forms import RegisterForm, LoginForm, UpdateAccountForm
from flasklogin.models import Admin
from flask_login import login_user, logout_user, current_user, login_required

def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/images', image_fn)
    output_size = (125,125)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)
    return image_fn

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
        flash(f'Account created for {form.name.data} sucessfully!!', 'success')
        return redirect('/login')
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # for redirecting it to the original route from where the request came from
            next_page = request.args.get('next')
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

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        print(form.image.data)
        if form.image.data:
            image_file = save_image(form.image.data)
            print(image_file)
            current_user.image = image_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated successfully', 'success')
        return redirect('/account')
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    image = url_for('static', filename=f"images/{current_user.image}")
    return render_template('account.html', form=form, image=image)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
