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

    def __init__(self, username, email, phone):
        self.username = username
        self.email = email
        self.phone = phone

    def __repr__(self):
        #return {u'phone': self.phone}
        print "User -> repr"
        return str(self.phone)


class PoliceBoat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    boat_number = db.Column(db.String(60), unique=True)

    def __init__(self, boat_number):
        self.boat_number = boat_number

    def __repr__(self):
        return '<PoliceBoat:  #%r>' % self.boat_number


try:
    db.create_all()
except:
    pass

if __name__ == "__main__":
    """
    admin = User('admin', 'admin@example.com', "99999999")
    guest = User('guest', 'guest@example.com', "77777777")

    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
    """
    print "Users:",  User.query.all()
