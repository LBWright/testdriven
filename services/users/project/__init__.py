from flask import Flask
from flask_restful import Resource, Api
 
# initialize app
app = Flask(__name__)
api = Api(app)


# set config
app.config.from_object('project.config.DevelopmentConfig')

class UsersPing(Resource):
    def get(self):
        return {
                'status': 'success',
                'message': 'pong!'
        }


api.add_resource(UsersPing, '/users/ping')
