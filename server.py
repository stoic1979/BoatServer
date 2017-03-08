#
# main script for starting server
#

from flask import Flask, render_template, request

from flask_restful import Resource, Api, reqparse

from models import User, db, app
from utils import *

import os

# setup apis
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        users = []
        try:
            for user in User.query.all():
                users.append(user.serialize)
        except Exception as exp:
            print "=============> got exp", exp

        ret = { "err": 0, "users": users}
        return ret, 201


class PhoneResource(Resource):
    """
    resource for handling phone number registration etc.
    """

    def createUser(self, phone):
        
        print "Creating phone validation req.: ", phone

        verify_code = get_random_str(6)
        user = User(phone, verify_code)
        db.session.add(user)
        db.session.commit()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone')
        args = parser.parse_args()

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


class CodeResource(Resource):
    """
    resource for handling verification number checking etc.
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code')
        args = parser.parse_args()
        print "args:", args

        code = args['code']

        ret = {"err": 0, "msg": "Verification done"}

        return ret, 201

api.add_resource(PhoneResource, '/verify_phoneno')
api.add_resource(CodeResource, '/verify_code')
api.add_resource(HelloWorld, '/')

if __name__ == "__main__":
    #db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
