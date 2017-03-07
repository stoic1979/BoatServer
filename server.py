#
# main script for starting server
#

from flask import Flask, render_template, request

from flask_restful import Resource, Api, reqparse

from models import User, db, app

# setup apis
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class PhoneResource(Resource):

    def createUser(self, phone):
        
        print "Creating phone validation req.: ", phone

        user = User("", "", phone) 
        db.session.add(user)
        db.session.commit()

        # admin = User.query.filter_by(username='admin').first()

    def get(self):
        ret = { "err": 0, "users": User.query.all()}
        return ret, 201



    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone')
        args = parser.parse_args()
        print "args:", args

        phone = args['phone']

        self.createUser(phone)


        #TODO get 6 digit no. from db for given phone no.
        ret = {
                "err": 0, 
                "msg": "Received phone no., will send 6 digit verification code by SMS"
             }

        return ret, 201


class CodeResource(Resource):

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
    db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
