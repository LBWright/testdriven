from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy import exc

from project import db
from project.api.models import User


users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)


class UsersPing(Resource):
    def get(self):
        return {"status": "success", "message": "pong!"}


class UsersList(Resource):
    def get(self):
        """Get all users"""
        response_object = {
            "status": "success",
            "data": {"users": [user.to_json() for user in User.query.all()]},
        }
        return response_object, 200

    def post(self):
        """Create a single user"""
        post_data = request.get_json()
        response = {"status": "fail", "message": "Invalid payload."}

        if not post_data:
            return response, 400

        username = post_data.get("username")
        email = post_data.get("email")
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                db.session.add(User(username=username, email=email))
                db.session.commit()
                response["status"] = "success"
                response["message"] = f"{email} was added!"
                return response, 201
            else:
                response["message"] = "Sorry. That email already exists."
                return response, 400

        except exc.IntegrityError:
            db.session.rollback()
            return response, 400


class Users(Resource):
    def get(self, user_id):
        """Get single user details"""
        response = {"status": "fail", "message": "User does not exist"}
        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if not user:
                return response, 404
            else:
                response = {
                    "status": "success",
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "active": user.active,
                    },
                }
                return response, 200

        except ValueError:
            return response, 404


api.add_resource(UsersPing, "/users/ping")
api.add_resource(UsersList, "/users")
api.add_resource(Users, "/users/<user_id>")
