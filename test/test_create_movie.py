import json 

from test.BaseCase import BaseCase

class MovieCreateTest(BaseCase):
    def test_succesful_movie_create(self):
        email = "albornozseba01@gmail.com"
        password = "hola"
        user_payload = json.dumps({
            "email":email,
            "password":password
        })

        self.app.post('/auth/signup', headers = {"Content-type":"application/json"}, data = user_payload)
        response = self.app.post('/auth/login', headers={"Content-Type": "application/json"}, data= user_payload)

        login_token = response.json['token']

        movie_payload = {
            "name": "Star Wars: The Rise of Skywalker",
            "cast": ["Daisy Ridley", "Adam Driver"],
            "genres": ["Fantasy", "Sci-fi"]
        }

        response = self.app.post('/movies', headers = {"Content-type":"application/json", "Authorization" : f"Bearer {login_token}"}, data = json.dumps(movie_payload))

        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)