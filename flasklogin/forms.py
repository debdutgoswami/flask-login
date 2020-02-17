from flask_wtf import FlaskForm, RecaptchaField, CSRFProtect
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from flasklogin.models import Admin

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

    # custom validators if the email already exists in the database
    def validate_email(self, email):
        user = Admin.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f"That email already exists")