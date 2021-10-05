import requests

class TokenProvider:

    @staticmethod
    def generateToken():
        admin = {'email': 'admin@hotmail.com', 'password': '1234'}
        response = requests.post('https://smart-feed-app.herokuapp.com/users/authenticate', json=admin)

        return response.json()['token']