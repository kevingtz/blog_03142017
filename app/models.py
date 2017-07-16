# HERE ARE THE DEFINED MODELS

from datetime import datetime
import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class Permission:  # THE DIFFERENT PERMISSIONS AROUND THE BLOG
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):  # THIS IS THE MODEL FOR THE ROLES
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')  # THIS MODEL GONNA BE A RELATION

    @staticmethod
    def insert_roles():  # UPDATE THE PERMISSIONS OR IF IT DOESNT EXISTS CREATE A NEW ONE
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)

        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


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
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())  # THE DIFFERENCE BETWEEN TEXT FIELD AND STRING FIELD IS THAT TEXT DOES NOT NEED
    # A MAXIMUM LENGTH
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)  # NOTE THAT IT IS MISSING THE '()' IN UTCNOW
    # THAT'S BECAUSE THE COLUMN'S ARGUMENT TAKES A FUNCTION AS A DEFAULT VALUE
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)  # SO EACH TIME DEFAULT VALUE NEEDS TO BE GENERATED
    # THE FUNCTION IS INVOKED TO PRODUCE IT.

    def __init__(self, **kwargs):  # ROLE ASSIGNMENT USING THE CURRENT_APP USER EMAIL
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['BLOG_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):  # THIS METHOD ASSERT THAT THE PASSWORD IS READABLE
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):  # THIS METHOD IS USING TO GENERATE THE HASH OF THE PASSWORD
        self.password_hash = generate_password_hash(password)

    def ping(self):  # THIS IS USED IN ORDER TO UPDATE THE LAST SINCE PROPERTY EACH TIME USER COMES. THIS METHOD IS
        # USED FOR 'BEFORE_APP_REQUEST' TO WORK
        self.last_seen = datetime.utcnow()
        db.session.add(self)

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

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, peermissions):
        return False

    def is_adminstrtor(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):  # THIS METHOD SEARCH A USER IN THE DB
    return User.query.get(int(user_id))
