# services/users/project/__init__.py

import sys
import os
from flask import Flask
from flask_restful import Resource, Api

# initialize app
app = Flask(__name__)
api = Api(app)


# set config
app_settings = os.getenv("APP_SETTINGS")
app.config.from_object(app_settings)


class UsersPing(Resource):
    def get(self):
        return {"status": "success", "message": "pong!"}


api.add_resource(UsersPing, "/users/ping")
