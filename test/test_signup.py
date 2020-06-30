import json

from index import app
from test.BaseCase import BaseCase


class SignupTest(BaseCase):
    def test_successful_signup(self):
        # Given
        payload = json.dumps({
            "email": "albornozseba01@gmail.com",
            "password": "hola"
        })

        # When
        response = self.app.post('/auth/signup', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)