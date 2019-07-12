import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import User


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong!", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self):
        """Ensure a new user can be added to the databse."""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"username": "logan", "email": "logan@gmail.com"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("logan@gmail.com was added!", data["message"])
            self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if JSON object is empty."""
        with self.client:
            response = self.client.post(
                "/users", data=json.dumps({}), content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_invalid_keys(self):
        """Ensure error is thrown if JSON object does not have username key."""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"email": "logan@gmail.com"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if email already exists."""
        with self.client:
            self.client.post(
                "/users",
                data=json.dumps({"username": "logan", "email": "logan@gmail.com"}),
                content_type="application/json",
            )
            response = self.client.post(
                "/users",
                data=json.dumps({"username": "logan", "email": "logan@gmail.com"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Sorry. That email already exists", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user("logan", "logan@gmail.com")

        with self.client:
            response = self.client.get(f"/users/{user.id}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("logan", data["data"]["username"])
            self.assertIn("logan@gmail.com", data["data"]["email"])
            self.assertIn("succes", data["status"])

    def test_single_user_no_id(self):
        """Ensure error is thrown if id is not provided"""
        with self.client:
            response = self.client.get("/users/testytest")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if id is not provided"""
        with self.client:
            response = self.client.get("/users/1000")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_all_users(self):
        """Ensure get all users behaves correctly"""
        add_user("logan", "logan@gmail.com")
        add_user("taylor", "taylor@gmail.com")
        with self.client:
            response = self.client.get("/users")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]["users"]), 2)
            self.assertIn("logan", data["data"]["users"][0]["username"])
            self.assertIn("logan@gmail.com", data["data"]["users"][0]["email"])
            self.assertIn("taylor", data["data"]["users"][1]["username"])
            self.assertIn("taylor@gmail.com", data["data"]["users"][1]["email"])
            self.assertIn("success", data["status"])

    def test_main_no_users(self):
        """Ensure the index route behaves correctly when no users exist."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"All Users", response.data)
        self.assertIn(b"<p>No users!</p>", response.data)

    def test_main_with_users(self):
        """Ensure main route behaves correctly when users exist."""
        add_user("logan", "logan@gmail.com")
        add_user("taylor", "taylor@gmail.com")
        with self.client:
            response = self.client.get("/")
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(b"logan", response.data)
            self.assertIn(b"taylor", response.data)

    def test_main_add_user(self):
        """Ensure a new user can be added to the db via a POST request"""

        with self.client:
            response = self.client.post(
                "/",
                data=dict(username="logan", email="logan@gmail.com"),
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(b"logan", response.data)


if __name__ == "__main__":
    unittest.main()
