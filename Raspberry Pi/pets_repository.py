import requests
import json

from token_provider import TokenProvider

class PetsRepository:

    @staticmethod
    def getFeeds (userId):
        token = TokenProvider.generateToken()
        headers = {'Authorization': f"Bearer {token}"}
        response = requests.get('https://smart-feed-api.herokuapp.com/pets/findByOwner/'+str(userId), headers = headers)

        return response