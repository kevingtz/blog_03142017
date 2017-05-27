# HERE ARE THE DEFINED MODELS

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class Role(db.Model):  # THIS IS THE MODEL FOR THE ROLES
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')  # THIS MODEL GONNA BE A RELATION

    def __repr__(self):  # THESE METHOD IS TO REPRESENT THE MODEL IN A STRING
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):  # THIS IS THE MODEL FOR THE USERS
    __tablename__ = 'users'  # THIS IS THE NAME OF THE TABLE NAME IN THE DB. SQLALCHEMY DEFINES THIS BY DEFAULT
    # IF THERE ARE NO NAMES SET
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # THIS IS A RELATION DATA KIND
    password_hash = db.Column(db.String(128))  # THIS DATA WILL BE USE BY THE PASSWORD METHOD IN ORDER TO GENERATE
    # A HASH
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):  # THIS METHOD ASSERT THAT THE PASSWORD IS READABLE
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):  # THIS METHOD IS USING TO GENERATE THE HASH OF THE PASSWORD
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):  # THIS METHOD IS TO VALIDATE THAT THE PASSWORD HASH
        # IS A REFERENCE OF THE PASSWORD
        return check_password_hash(self.password_hash, password)

    def generation_confirmed_token(self, expiration=3600):  # THIS FUNCTION GENERATES A TOKEN
        # THE EXPIRATION ARGUMENT CAN BE SET
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):  # THIS FUNCTION ASSERT THAT IN FACT THE TOKEN WILL BE RECIP DOESN'T BE EXPIRATED AND ALSO
        # THAT WAS THE SAME WE SENT IN THE MAIL
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)  # HERE WE ASSERT IT DOESN'T EXPIRED
        except:  # ANY KIND OF EXCEPTION WILL BE RETURN FALSE
            return False
        if data.get('confirm') != self.id:  # HERE WE ASSERT IT IS THE SAME TOKEN
            return False
        self.confirmed = True
        db.session.add(self)  # IF ALL IS OK WE ADD THE SESSION TO THE DB
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return  False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):  # THIS METHOD SEARCH A USER IN THE DB
    return User.query.get(int(user_id))
