import requests
import json

from token_provider import TokenProvider

class ConsumptionsRepository:

    @staticmethod
    def getFeeds ():
        token = TokenProvider.generateToken()
        headers = {'Authorization': f"Bearer {token}"}
        response = requests.get('https://smart-feed-app.herokuapp.com/feeds', headers = headers)

        return response