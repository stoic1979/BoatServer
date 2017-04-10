#
# main script for starting server
#

from flask import Flask, render_template, request

from flask_restful import Resource, Api, reqparse

from models import User, Boat, Report, Likes, Thanks, db, app
from utils import *
from flask import jsonify 
import traceback
from math import sin, cos, atan2, sqrt, radians
import os
import json

lng1 = radians(21.012287)
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
#api.add_resource(PhoneResource, '/verify_phoneno')
#api.add_resource(CodeResource, '/verify_code')
api.add_resource(HomeResource, '/')


def createUser(phone):
        
    print "Creating phone validation req.: ", phone

    vcode = get_random_str(6)
    user = User(phone, vcode)
    db.session.add(user)
    db.session.commit()

@app.route("/verify_phoneno" , methods=['POST'])
def verify_phoneno():

    ret = {"err": 0, "msg": "Received phone no., will send 6 digit verification code by SMS"}

    phone = request.form['phone']

    # ensure that phone no. doesn't exist
    if User.query.filter_by(phone=phone).first():
        ret["err"] = 1
        ret["msg"] = "Phone no. already exist"
    else:
        createUser(phone)

    return json.dumps(ret)



@app.route("/verify_code" , methods=['POST'])
def verify_code():
    ret = {"err": 0, "msg": "Verification done" }

    phone = request.form['phone']
    vdone = True

    # checking verification code
    user = User.query.filter_by(phone=phone).first()
    if not user:
        ret["err"] = 1
        ret["msg"] = "Invalid phone numner"
    elif user.vdone == True:
        ret["err"] = 2
        ret["msg"] = "Verification already done !!!"
    else:
        user.vdone = True
        db.session.add(user)
        db.session.commit()

    return json.dumps(ret)


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
    print "===================save_police_boat :", request.form
    try:
        boat_name = request.form['boat_name']
        btype = request.form['btype']
        #boat = Boat("assd", 1234)
        boat = Boat(boat_name, btype)
        db.session.add(boat)
        db.session.commit()
    except Exception as exp:
        print "=============> got exp", exp
        print(traceback.print_stack())
    return "boat_name: %s is saved" % (boat_name)

@app.route("/location")
def location():
    templateData = {'title' : 'Home Page'}
    return render_template("location.html", **templateData )

"""@app.route("/save_location", methods=['POST'])
def save_location():
    boat = request.form['Police_boat']
    lat = request.form['lat']
    lng = request.form['lng']
    #police_boat_location = Report(1,11,111)
    police_boat_location = Report(boat, lat,lng)
    db.session.add(police_boat_location)
    db.session.commit()
    return "Location: %s is saved" % (police_boat_location)
"""



@app.route("/add_profile", methods=['POST'])
def add_profile():
    print "======add_profile()::",request.form
    try:
        Nickname = request.form['nickname']
        Town = request.form['town']
        District = request.form['district']
        Dob = request.form['dob']
        Boatinfo = request.form['boatinfo']
        Profile = User(Nickname, Town, District, Dob, Boatinfo)
        db.session.add(Profile)
        db.session.commit()
    except Exception as exp:
        print "exp:", exp
        print(traceback.format_exc())
    return "Profile Added"


def get_report_like_count(report_id):
    counter = 0
    likesreport = Likes.query.all()
    for likes in likesreport:
        if report_id == likes.report:
            counter +=1
    return counter

@app.route("/get_like_count", methods=['POST'])
def get_like_count():

    ret = {"likes_count": 0, "report_id": 0, "error": 0}  

    try:
        report_id = int(request.form['report_id'])
        ret["report_id"] = report_id
        ret["likes_count"] = get_report_like_count(report_id)
    except Exception as exp:
        print "exp:", exp
        print(traceback.format_exc())
        ret["error"] = 1
        ret["msg"] = "Got exception: %s" % exp

    return json.dumps(ret)



@app.route("/add_like", methods=['POST'])
def add_like():
    try:
        likeReportId = int(request.form['report_id'])
        likeUserId = int(request.form['user_id'])
        value = int(request.form['value'])
        like = Likes(likeReportId, likeUserId, value)
        db.session.add(like)
        db.session.commit()
    except Exception as exp:
        print "exp:", exp
        print(traceback.format_exc())
    return "Likes Add"


@app.route("/add_thanks", methods=['POST'])
def add_thanks():
    try:
        report_id = request.form['thanks_report_id']
        user_id = request.form['thanks_user_id']
        thanks = Thanks(report_id, user_id)
        db.session.add(thanks)
        db.session.commit()
    except Exception as exp:
        print "exp:", exp
        print(traceback.format_exc())
    return "Thanks Added"

@app.route("/save_reports", methods=['POST'])
def save_reports():
    print "=====save_reports():==", request.form
    try:
        boat_name = request.form['boat_name']
        boat_type = int(request.form['boat_type'])
        get_lat = request.form['get_lat']
        get_lng = request.form['get_lng']
        user_id = int(request.form['user_id'])
        savereport = Report(boat_name, boat_type, get_lat, get_lng, user_id)
        db.session.add(savereport)
        db.session.commit()
    except Exception as exp:
        print "exp:", exp
        print(traceback.format_exc())
    return "Save Reports.."

@app.route("/get_report", methods=['POST'])
def get_report():
    print "======== get_report() : ======= ", request.form
    try:
        lat = request.form['get_lat']
        lng = request.form['get_lng']
        radius = request.form['radius']
        print "latitude : %s " % lat
        #R = 6373.0 
        # approximate radius of earth in KM

        lat1 = radians(lat)
        lng1 = radians(lng)
        lat2 = radians(52.406374)
        lng2 = radians(16.9251681)

        dlng = lng2 - lng1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        distance = radius * c

        print ("Result", distance)
        #print ("Should be :", 278.546,"km")
    except Exception as exp:
        print "exp:",exp
        print(traceback.format_exc())
    return "done"

@app.route("/get_distance")
def  get_distance():
    print "Going to calculate distance between given longitudes and latitudes"

    report_distance = Report.query.all()
    for report in report_distance:
        print "===========" , report.boat_name
    R = 6373.0 
    # approximate radius of earth in KM

    lat1 = radians(30.74659)
    lng1 = radians(76.78532)
    lat2 = radians(30.69479)
    lng2 = radians(76.79876)

    dlng = lng2 - lng1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    distance = R * c * 100056

    print ("Result", distance)
    print ("Should be :", 278546,"m")
    return "distance : %d"  % distance

 

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
