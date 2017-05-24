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

from utils import dlog

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
            print( "=============> got exp", exp)
            traceback.print_stack()


        ret = { "err": 0, "users": users}
        return ret, 201


class PhoneResource(Resource):
    """
    resource for handling phone number registration etc.
    """

    def createUser(self, phone):
        
        print ("Creating phone validation req.: ", phone)

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
        #return json.dumps(ret)

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
#api.add_resource(PhoneResourc)
#api.add_resource(CodeResource, '/verify_code')
api.add_resource(HomeResource, '/')


def createUser(phone):
        
    print ("Creating phone validation req.: ", phone)

    vcode = get_random_str(6)
    user = User(phone, vcode)
    db.session.add(user)
    db.session.commit()

    #dlog("user id: %d" % user.id)
    print ("user id:===> : %d" % user.id)

    return user.id

@app.route("/verify_phoneno" , methods=['POST'])
def verify_phoneno():

    ret = {"err": 0, "msg": "Received phone no., will send 6 digit verification code by SMS"}

    """
    user = User.query.filter_by(phone=phone).first()
    

    
    for user in User.query.all():
        user = User.query.filter_by(phone=phone).first()
    print "user id:===> : %d" % user.id

    #
    """
    phone = request.form['phoneno']



    dlog("Verigfuying phone no.: %s" % phone)

    # ensure that phone no. doesn't exist
    if User.query.filter_by(phone=phone).first():
        ret["err"] = 1
        ret["msg"] = "Phone no. already exist"
    else:
        ret["uid"] = createUser(phone)

    return json.dumps(ret)



@app.route("/verify_code" , methods=['POST'])
def verify_code():
    ret = {"err": 0, "msg": "Verification done" }

    phone = request.form['phoneno']
    vcode = request.form['vcode']
    vdone = True

    # checking verification code
    user = User.query.filter_by(phone=phone).filter_by(vcode=vcode).first()
    if not user:
        ret["err"] = 1
        ret["msg"] = "Invalid phone numner"

    elif user.vdone == True:
        ret["err"] = 2
        ret["msg"] = "Verification already done !!!"
    else:
        ret["uid"] = user.id
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
    print ("===================save_police_boat :", request.form)
    try:
        boat_name = request.form['boat_name']
        btype = request.form['btype']
        #boat = Boat("assd", 1234)
        boat = Boat(boat_name, btype)
        db.session.add(boat)
        db.session.commit()
    except Exception as exp:
        print ("=============> got exp", exp)
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
    print ("======add_profile()::",request.form)
    ret = {"err": 0, "msg": "Usesr profile is saved"}
    
    try:
        uid = int(request.form['uid'])
        nickname = request.form['nickname']
        town = request.form['town']
        district = request.form['district']
        dob = request.form['dob']
        boatinfo = request.form['boatinfo']
        user = User.query.filter_by(id=uid).first()

        if not user:
            ret["err"] = 2
            ret["msg"] = "User not found with given id=%d" % uid
        else:
            user.nickname = nickname
            user.town = town
            user.district = district
            user.dob = dob
            user.boatinfo = boatinfo

            # save and update user 
            db.session.add(user)
            db.session.commit()
            ret["profile"] = user.serialize
    except Exception as exp:
        print ("exp:", exp)
        print(traceback.format_exc())
        ret["err"] = 1 
        ret["msg"] = "Got exception %s" % exp
     
    return json.dumps(ret)

@app.route("/set_iap", methods=['POST'])
def set_iap():
    ret = {"err": 0, "msg": "IAP is saved in Usesr profile"}
    try:
        user_id = int(request.form["user_id"])
        value = int(request.form["value"])
        user = User.query.filter_by(id=user_id).first()
        if not user:
            ret["err"] = 2
            ret["msg"] = "User not found with given id=%d" % user_id
        else:
            user.value = value

            # save and update user 
            db.session.add(user)
            db.session.commit()
            ret["User Id"] = user_id
            ret["Flag Value"] = user.value
    except Exception as exp:
        print ("exp:", exp)
        print(traceback.format_exc())
        ret["err"] = 1 
        ret["msg"] = "Got exception %s" % exp
    return json.dumps(ret)


@app.route("/get_iap", methods=['POST'])
def get_iap():
    ret = {"error": 0}
    try:
        user_id = int(request.form["user_id"])
        user = User.query.filter_by(id=user_id).first()
        if not user:
            #ret["err"] = 2
            ret["msg"] = "User not found with given id=%d" % user_id
            ret["Flag"] = 0
        else:
            ret["Flag"] = user.value
    except Exception as exp:
        print ("exp:", exp)
        print(traceback.format_exc())
        ret["err"] = 1 
        ret["msg"] = "Got exception %s" % exp
    return json.dumps(ret)



@app.route("/get_user", methods=['POST'])
def get_user():
    print ("+++====+get_user+==>>:", request.form)
    ret = {"err": 0, "msg": "Get the User Details"}
    user_id = request.form['user_id']
    user = User.query.filter_by(id=user_id).first()
    if not user:
        ret["err"] = 1
        ret["msg"] = "User not found with given id = %s" % user_id
    else:
        ret["User"] = user.serializes
    return json.dumps(ret)


def get_report_like_count(report_id):
    counter = 0
    likesreport = Likes.query.filter_by(value=1).filter_by(report=report_id).all()
    
    for likes in likesreport:
        if report_id == likes.report:
            counter +=1
    return counter

def get_report_dislike_count(report_id):
    counter = 0
    likesreport = Likes.query.filter_by(value=0).all()
    for likes in likesreport:
        if report_id == likes.report:
            counter +=1
    return counter


@app.route("/get_like_count", methods=['POST'])
def get_like_count():

    ret = {"error": 0}  

    try:
        report_id = int(request.form['report_id'])
        user_id = int(request.form["user_id"])
        ret["report_id"] = report_id
        ret["likes_count"] = get_report_like_count(report_id)
        ret["dislike_count"] = get_report_dislike_count(report_id)
        like = Likes.query.filter_by(report=report_id).filter_by(user=user_id).first()
        if not like:
            ret["Like Value"] = 0
            ret["flag"] = 0
            #ret["User Id"] = user_id    
        else:
            ret["Like Value"] = like.value
            ret["flag"] = like.flag
            ret["User Id"] = user_id
        # ret["likes_count of a user"] = get_user_like_count(user_id)
        # ret["dislike_count of a user"] = get_user_dislike_count(user_id)
        #likes= Likes.query.filter_by(user=user_id).first()
    except Exception as exp:
        print ("exp:", exp)
        print(traceback.format_exc())
        ret["error"] = 1
        ret["msg"] = "Got exception: %s" % exp
    return json.dumps(ret)



@app.route("/add_like", methods=['POST'])
def add_like():
    ret = {"error": 0}
    try:
        report_id = int(request.form['report_id'])
        user_id = int(request.form['user_id'])
        value = int(request.form['value'])
        flag_value = int(request.form["flag_value"])
        
        # check if like for same report exists by this user
        like = Likes.query.filter_by(user=user_id).filter_by(report=report_id).first()
        if like:
            print "[add_like] User already had liked/disliked this report"
            like.value = value
           
        else:
            like = Likes(report_id, user_id, value, flag_value)

        db.session.add(like)
        db.session.commit()
        ret["msg"] = "The Like and flag is added successfully"
    except Exception as exp:
        print ("exp:", exp)
        print(traceback.format_exc())
        ret["error"] = 1
        ret["msg"] = "Got exception: %s" % exp
    return json.dumps(ret)


def get_user_like_count(user_id):
    counter = 0
    likesreport = Likes.query.filter_by(value=1).all()
    
    for likes in likesreport:
        if user_id == likes.user:
            counter +=1
    return counter

def get_user_dislike_count(user_id):
    counter = 0
    likesreport = Likes.query.filter_by(value=0).all()
    for likes in likesreport:
        if user_id == likes.user:
            counter +=1
    return counter

@app.route("/users_likes_dislikes", methods=['POST'])
def user_likes_dislikes():
    ret = {"error": 0}
    try:
        user_id = int(request.form['user_id'])
        ret["User_id"] = user_id
        ret["likes_count"] = get_user_like_count(user_id)
        ret["dislike_count"] = get_user_dislike_count(user_id)
        thanks_count = Thanks.query.filter_by(value=1).all()
        for thanks in thanks_count:
            if user_id == thanks.user:
                ret["Thanks"] = thanks.value
    except Exception as exp:
        print ("exp:", exp)
        print(traceback.format_exc())
    return json.dumps(ret)


@app.route("/add_thanks", methods=['POST'])
def add_thanks():
    ret = {"error": 0}
    try:
        report_id = int(request.form['thanks_report_id'])
        user_id = int(request.form['thanks_user_id'])
        flag_value = int(request.form['flag_value'])

        # check if flag for same report exists by this user
        thanks = Thanks.query.filter_by(user=user_id).filter_by(report=report_id).first()
        if thanks:
            print "[add_thanks] User already had liked/disliked this report"
            thanks.value = flag_value
        else:
            thanks = Thanks(report_id, user_id, flag_value)
        db.session.add(thanks)
        db.session.commit()
        ret["msg"] = "The Flag is added successfully"
    except Exception as exp:
        print ("exp:", exp)
        print(traceback.format_exc())
        ret["error"] = 1
        ret["msg"] = "Got exception: %s" % exp
    return json.dumps(ret)


@app.route("/total_thanks", methods=['POST'])
def total_thanks():
    ret = {"error": 0}
    try:
        report_id = int(request.form['report_id'])
        user_id = int(request.form['user_id'])
        counter = 0
        thanks = Thanks.query.all()
        thank = Thanks.query.filter_by(report=report_id).first()
        if not thank:
            ret["error"] = 1
            ret["msg"] = "Invaild Report Id Entered by user"
        else:
            thanks_total = Thanks.query.all()
            for thanks in thanks_total:
                if report_id == thanks.report:
                    counter +=1
                    ret["Total Thanks"] = counter
                    ret["Report Id"] = thanks.report
                    # ret["flag"] = thanks.value
                    # ret["User Id"] = user_id
        thankflag = Thanks.query.filter_by(report=report_id).filter_by(user=user_id).first()
        if not thankflag:
            ret["Flag"] = 0
        else:
            ret["flag"] = thankflag.value
            ret["User Id"] = user_id
    except Exception as exp:
        print ("exp:", exp)
        print(traceback.format_exc())
    return json.dumps(ret)

@app.route("/save_reports", methods=['POST'])
def save_reports():
    print ("=====save_reports():==", request.form)
    ret = {"err": 0, "msg": "Report id is save"}
    getreport = Report.query.all()
    for report in getreport:
        print ("fatching Report name :", report.boat_name)
        print ("fatching Report boat type :", report.boat_type)
        print ("fatching Report lat :", report.lat)
        print ("fatching Report lng :", report.lng)
        print ("fatching Report user :", report.user)
    try:
        #boat_id = int(request.form['boat_id'])
        boat_name = request.form['boat_name']
        boat_type = request.form['boat_type']
        get_lat = request.form['get_lat']
        get_lng = request.form['get_lng']
        user_id = int(request.form['user_id'])

        # boatcheck = Boat.query.filter_by(id=boat_id).first()
        # if not boatcheck:
        #     ret["err"] = 1
        #     ret["msg"] = "Boat is not exist"
        # else:
        #     # saving report
        #     report.boat = boat_id
        report = Report(boat_name, boat_type, get_lat, get_lng, user_id)
        db.session.add(report)
        db.session.commit()
        ret["report_id"] = report.id
    except Exception as exp:
        print ("exp:", exp)
        print(traceback.format_exc())
    return json.dumps(ret)

# @app.route("/report_fatching")
# def report_fatching():
#     reports = []
#     getreport = Report.query.all()
#     for report in getreport:
#         reports.append(report.serialize)
#         print "fatching Report name :", report.boat_name
#         print "fatching Report boat type :", report.boat_type
#         print "fatching Report lat :", report.lat
#         print "fatching Report lng :", report.lng
#         print "fatching Report user id :", report.user
#         ret = { "err": 0, "reports": reports}
#     return json.dumps(ret)

@app.route("/get_report", methods=['POST'])
def get_report():
    print ("======== get_report() : ======= ", request.form)
    ret = { "err": 0, "reports": []}
    try:
        lat = float(request.form['lat'])
        lng = float(request.form['lng'])
        radius = float(request.form['radius'])
        reports = []
        #getreport = Report.query.all()
        #print "getreport: ", getreport
        #print

        query = "SELECT DISTINCT boat_name,boat_type,lat,lng,user, id, ts FROM report where ts > NOW() - INTERVAL 24 HOUR"

        connection = db.session.connection()

        records = connection.execute(query)

        print ("========>>>> records: ", records)

        for record in records.fetchall():
            distance = get_geo_distance(lat, lng, record["lat"], record["lng"])
            print ("---- record:", record)
            print ("distance:", distance, " radius:", radius)
            if distance <= radius:
                #print "adding report", report
                item = {}
                item["boat_name"] = record["boat_name"]
                item["boat_type"] = record["boat_type"]
                item["lat"] = record["lat"]
                item["lng"] = record["lng"]
                item["id"] = record["id"]
                item["user"] = record["user"]
                item["ts"] = str(record["ts"])
                reports.append(item)

        ret["reports"] = reports
    except Exception as exp:
        print ("[get_report] :: exp:", exp)
        print(traceback.format_exc())
        ret["err"] = 1
        ret["msg"] = "Report Error"
    return json.dumps(ret)

def get_geo_distance(lat1, lng1, lat2, lng2):
    R = 6373.0
    dlng = lng2 - lng1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c * 1000

@app.route("/get_distance")
def get_distance():
    print ("Going to calculate distance between given longitudes and latitudes")

    report_distance = Report.query.all()
    for report in report_distance:
        print ("===========" , report.boat_name)
    R = 6373.0 
    # approximate radius of earth in KM

    lat1 = radians(30.74659)
    lng1 = radians(76.78532)
    lat2 = radians(30.69479)
    lng2 = radians(76.79876)

    distance = get_geo_distance(lat1, lng1, lat2, lng2)

    print ("Result", distance)
    print ("Should be :", 278546,"m")
    return "distance : %d"  % distance

 

@app.route("/get_police_boats")
def get_police_boats():

    boats = PoliceBoat.query.all()
    for boat in boats:
        print ("Boat Number: ", boat.boat_number)

    return "get the police Boat"
#get_police_boat_locations

@app.route("/get_police_boat_locations")
def get_police_boat_locations():
    boat_locations = PoliceBoatLocation.query.all()
    for location in boat_locations:
        print ("Police Boat Location: ", location.police_boat)
        print ("Police Boat Location: ", location.lat)
        print ("Police Boat Location: ", location.lng)
    return "get police boat locations"




#################################################################
#                                                               #
#                           SERVER MAIN                         #
#                                                               #
#################################################################
if __name__ == "__main__":
    #db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
