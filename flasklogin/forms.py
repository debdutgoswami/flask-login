from flask_wtf import FlaskForm, RecaptchaField, CSRFProtect
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('username', validators=[InputRequired(), Length(max=50), Email(message='Invalid Email')], id='email')
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)], id='psd')
    remember = BooleanField('remember me', id='remember')
    #recaptcha = RecaptchaField()
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(min=4, max=50)], id='name')
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)], id='email')
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)], id='psd')
    confirm_password = PasswordField('confirm password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('password', message="Paswords should match")], id='cnfpsd')
    #recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')