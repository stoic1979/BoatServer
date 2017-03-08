#
# script for various ORM models for project
#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boatdb.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    email = db.Column(db.String(60), unique=True)
    phone = db.Column(db.String(16), unique=True)
    verification_code = db.Column(db.String(6))


    def __init__(self, phone, verification_code):
        #TODO do we need username or email ??
        self.phone = phone
        self.verification_code = verification_code

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'phone': self.phone,
           'verification_code': self.verification_code
       }


class PoliceBoat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    boat_number = db.Column(db.String(60), unique=True)

    def __init__(self, boat_number):
        self.boat_number = boat_number

    def __repr__(self):
        return '<PoliceBoat:  #%r>' % self.boat_number


try:
    print "================================= create_all ==================================="
    db.create_all()
except:
    pass


################################
#                              #
#       SOME QUICK TESTS       #
#                              #
################################
if __name__ == "__main__":
    """
    user = User("77777777", "abc123")
    db.session.add(user)
    db.session.commit()
    """
    print "Users:",  User.query.all()
