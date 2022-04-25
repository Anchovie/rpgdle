from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash
from .extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    participations = db.relationship("Participation", backref="user", lazy=True, primaryjoin="User.id == Participation.user_id")

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
                #"participations": self.participations.serialize}

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.admin}', )"

class Doodle(db.Model):
    __tablename__ = 'Doodle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    time = db.Column(db.String(20))
    old = db.Column(db.Boolean)
    creator = db.Column(db.Integer, db.ForeignKey("user.id"))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    dates = db.Column(db.Text)

    participations = db.relationship("Participation", cascade="all, delete, delete-orphan", backref = "doodle", lazy=True, , primaryjoin="Doodle.id == Participation.doodle_id")
    #    participations = db.relationship("Participation", cascade="all, delete-orphan", """backref = db.backref("doodle", cascade="all, delete-orphan"),""" lazy=True)

    #dates = db.Column(db.ARRAY(db.DateTime))
    #dates = db.relationship("Date", backref="belongsTo")
    #attendees = db.Column(db.ARRAY(db.ARRAY(db.ForeignKey("user.id"))))

class Participation(db.Model):
    __tablename__ = 'Participation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    doodle_id = db.Column(db.Integer, db.ForeignKey("doodle.id")) #relationship("Doodle",onDelete="CASCADE")
    date = db.Column(db.String(20))
    status = db.Column(db.String(10))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {"user": self.user_id,
                "doodle": self.doodle_id,
                "date": self.date,
                "status": self.status}

'''
class Date(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, primary_key=True)
    #attendees = db.ARRAY(db.ForeignKey("user.id"))
    attendees = db.relationship("User", backref="acceptedDate")

    #responders = db.Column()
    #days =
'''
