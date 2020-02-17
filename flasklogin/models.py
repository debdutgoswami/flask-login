from flasklogin import db, loginmanager
from flask_login import UserMixin

@loginmanager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(180), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"