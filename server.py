#
# main script for starting server
#

from flask import Flask, render_template, request

from flask_restful import Resource, Api, reqparse

from models import User, PoliceBoat, PoliceBoatLocation, db, app
from utils import *

import traceback

import os

# setup REST apis
api = Api(app)

class HomeResource(Resource):
    def get(self):
        users = []
        try:
            for user in User.query.all():
                users.append(user.serialize)
        except Exception as exp:
            print "=============> got exp", exp
            traceback.print_stack()


        ret = { "err": 0, "users": users}
        return ret, 201


class PhoneResource(Resource):
    """
    resource for handling phone number registration etc.
    """

    def createUser(self, phone):
        
        print "Creating phone validation req.: ", phone

        verification_code = get_random_str(6)
        user = User(phone, verification_code)
        db.session.add(user)
        db.session.commit()

    def post(self):

        # initializing post args parser
        parser = reqparse.RequestParser()
        parser.add_argument('phone')
        args = parser.parse_args()

        # reading post args
        phone = args['phone']

        ret = {
                "err": 0, 
                "msg": "Received phone no., will send 6 digit verification code by SMS"
             }

        # ensure that phone no. doesn't exist
        if User.query.filter_by(phone=phone).first():
            ret["err"] = 1
            ret["msg"] = "Phone no. already exist"
        else:
            self.createUser(phone)

        return ret, 201


class PoliceBoatResource(Resource):
    """
    resource for handling police boat records
    """

    def post(self):

        # initializing post args parser
        parser = reqparse.RequestParser()
        parser.add_argument('lat')
        parser.add_argument('lng')
        args = parser.parse_args()

        # reading position vars
        lat = args['lat']
        lng = args['lng']

        ret = {
                "err": 0, 
                "msg": "police boat added"
             }

        return ret, 201


class CodeResource(Resource):
    """
    resource for handling verification number checking etc.
    """

    def post(self):

        # initializing post args parser
        parser = reqparse.RequestParser()
        parser.add_argument('verification_code')
        parser.add_argument('phone')
        args = parser.parse_args()

        # reading post args
        phone = args['phone']
        verification_code = args['verification_code']

        ret = {
                "err": 0, 
                "msg": "Verification done"
                }

        # checking verification code
        if not User.query.filter_by(phone=phone).filter_by(verification_code=verification_code).first():
            ret["err"] = 1
            ret["msg"] = "Verification with 6 digit code failed, pls check the code"

        return ret, 201

# setting up URL end point handlers
api.add_resource(PhoneResource, '/verify_phoneno')
api.add_resource(CodeResource, '/verify_code')
api.add_resource(HomeResource, '/')

# add police boat
@app.route("/add_police_boat" , methods=['POST'])
def add_police_boat():
    return "add police boat"

@app.route("/api_demo")
def apidemo():
    templateData = {'title' : 'Home Page'}
    return render_template("api_demo.html", **templateData )

@app.route("/save_police_boat", methods=['POST'])
def api_post():

    boat_number = request.form['boat_number']
    
    police_boat = PoliceBoat(boat_number)
    db.session.add(police_boat)
    db.session.commit()
    return "boat_number: %s is saved" % (boat_number)

@app.route("/location")
def location():
    templateData = {'title' : 'Home Page'}
    return render_template("location.html", **templateData )

@app.route("/save_location", methods=['POST'])
def save_location():
    Police_boat = request.form['Police_boat']
    lat = request.form['lat']
    lng = request.form['lng']
    police_boat_location = PoliceBoatLocation(Police_boat,lat,lng)
    db.session.add(police_boat_location)
    db.session.commit()
    return "Location: %s is saved" % (police_boat_location)

@app.route("/save_like_report", methods=['POST'] )
def save_like_report():
    return "hiiii its done"


#get_police_boats

@app.route("/get_police_boats")
def get_police_boats():

    boats = PoliceBoat.query.all()
    for boat in boats:
        print "Boat Number: ", boat.boat_number

    return "get the police Boat"
#get_police_boat_locations

@app.route("/get_police_boat_locations")
def get_police_boat_locations():
    boat_locations = PoliceBoatLocation.query.all()
    for location in boat_locations:
        print "Police Boat Location: ", location.police_boat
        print "Police Boat Location: ", location.lat
        print "Police Boat Location: ", location.lng
    return "get police boat locations"


#################################################################
#                                                               #
#                           SERVER MAIN                         #
#                                                               #
#################################################################
if __name__ == "__main__":
    #db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
