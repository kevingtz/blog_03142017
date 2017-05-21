# HERE ARE THE DEFINED MODELS

from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')  # THIS MODEL GONNA BE A RELATION

    def __repr__(self):  # THESE METHOD IS TO REPRESENT THE MODEL IN A STRING
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.Foreignkey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username
