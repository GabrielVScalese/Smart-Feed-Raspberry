import os
from dotenv import load_dotenv

load_dotenv()

import requests

class TokenProvider:

    @staticmethod
    def generateToken():
        admin = {'email': os.getenv('EMAIL'), 'password': os.getenv('PASSWORD')}
        response = requests.post('https://smart-feed-app.herokuapp.com/users/authenticate', json=admin)

        return response.json()['token']