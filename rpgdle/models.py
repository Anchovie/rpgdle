from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash
from .extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    #participations = db.relationship("participation", backref="user", lazy=True, primaryjoin="user.id == participation.user_id")

    @property
    def unhashed_password(self):
        raise AttributeError("Cannot view unhashed password")

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "admin": (0,1)[self.admin]}

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.admin}', )"

class Doodle(db.Model):
    __tablename__ = 'doodle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    time = db.Column(db.String(20))
    old = db.Column(db.Boolean)
    creator = db.Column(db.Integer, db.ForeignKey("User.id"))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    dates = db.Column(db.Text)

    #participations = db.relationship("participation", cascade="all, delete, delete-orphan", backref = "doodle", lazy=True, primaryjoin="doodle.id == participation.doodle_id")

class Participation(db.Model):
    __tablename__ = 'participation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    doodle_id = db.Column(db.Integer, db.ForeignKey("Doodle.id"))
    date = db.Column(db.String(20))
    status = db.Column(db.String(10))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {"user": self.user_id,
                "doodle": self.doodle_id,
                "date": self.date,
                "status": self.status}
