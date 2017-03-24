#
# script for various ORM models for project
#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boatdb.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@localhost/boatappdb'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, primary_key=True)
    nickname = db.Column(db.String(60), unique=True)
    email = db.Column(db.String(60), unique=True)
    phone = db.Column(db.String(20), unique=True)
    town = db.Column(db.String(60))
    district = db.Column(db.String(16))
    dob = db.Column(db.Date)
    boatinfo = db.Column(db.String(120))

    # todo - work on picture feature of profile later !!!!!
    #pic =  

    # verification code
    vcode = db.Column(db.String(6))

    # verification done
    vdone = db.Column(db.Boolean, default=False)


    # timestamp
    ts = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)


    def __init__(self, phone):
        self.phone = phone


    def __repr__(self):
        return '<User:  #%r>' % self.id

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'phone': self.phone,
           'vcode': self.vcode
       }


class Boat(db.Model):
    """
    model for police boat
    """
    __tablename__ = 'boat'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(60), unique=True)

    # Boat type can be undercover cop or waterPolice boat
    btype = db.Column(db.Integer)

    # timestamp
    ts = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Boat:  #%r>' % self.name


class Report(db.Model):
    """
    model for police boat location
    """
    __tablename__ = 'report'

    id = db.Column(db.BigInteger, primary_key=True)
    boat = db.Column(db.BigInteger, ForeignKey('boat.id'))
    lat = db.Column(db.Float, unique=True)
    lng = db.Column(db.Float, unique=True)
    user = db.Column(db.BigInteger, ForeignKey('user.id'))

    # timestamp
    ts = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False )

    def __init__(self, boat, lat, lng, btype):
        self.boat = boat
        self.lat = lat
        self.lng = lng
        self.btype = btype

    def __repr__(self):
        return '<Report:  #%r>' % self.id


class Likes(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.BigInteger, primary_key=True)
    report = db.Column(db.BigInteger, ForeignKey('report.id'))
    user = db.Column(db.BigInteger, ForeignKey('user.id'))

    # timestamp
    ts = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)


    def __repr__(self):
        return '<Likes:  #%r>' % self.id


class Dislikes(db.Model):
    __tablename__ = 'dislikes'

    id = db.Column(db.BigInteger, primary_key=True)
    report = db.Column(db.BigInteger, ForeignKey('report.id'))
    user = db.Column(db.BigInteger, ForeignKey('user.id'))
    
    # timestamp
    ts = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)


    def __repr__(self):
        return '<Dislikes:  #%r>' % self.id


class Thanks(db.Model):
    __tablename__ = 'thanks'

    id = db.Column(db.BigInteger, primary_key=True)
    report = db.Column(db.BigInteger, ForeignKey('report.id'))
    user = db.Column(db.BigInteger, ForeignKey('user.id'))

# timestamp
    ts = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False )


    def __repr__(self):
        return '<Thanks:  #%r>' % self.id



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
