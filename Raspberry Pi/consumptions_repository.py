import requests
import json

from token_provider import TokenProvider

class ConsumptionsRepository:

    @staticmethod
    def createConsumption (feed):
        token = TokenProvider.generateToken()
        payload = {'Authorization': f"Bearer {token}"}
        response = requests.post('https://smart-feed-app.herokuapp.com/consumptions', json = feed, headers = payload)

        return response