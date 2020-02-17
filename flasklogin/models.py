from flasklogin import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(180), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"