from typing import Dict, List
import requests


class Covid19(object):
    url = ""

    def __init__(self, url="https://coronavirus-19-api.herokuapp.com"):
        self.url = url

    def _request(self, endpoint):
        response = requests.get(self.url + endpoint)
        response.raise_for_status()
        if response:
            return response.json()
        else:
            return False

    def getTotal(self) -> List[Dict[str, int]]:
        """
        :return: The latest amount of total confirmed cases, deaths, and recoveries.
        """
        data = self._request("/countries/World")
        return data

    def getByCountry(self, country) -> List[Dict]:
        data = self._request("/countries/{}".format(country))
        return data
