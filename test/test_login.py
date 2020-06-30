import json 

from test.BaseCase import BaseCase

class UserLoginTest(BaseCase):
    def test_succesful_login(self):
        email = "albornozseba01@gmail.com"
        password = "hola"
        payload = json.dumps({
            "email":email,
            "password":password
        })
        response = self.app.post('/auth/signup', headers = {"Content-type":"application/json"}, data = payload)

        response = self.app.post('/auth/login', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(str, type(response.json['token']))
        self.assertEqual(200, response.status_code)
