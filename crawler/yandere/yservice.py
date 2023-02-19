import requests
from pykson import Pykson
from .models.Tag import Tag


class YandereService:

    @staticmethod
    def search_tags(tag, limit):
        url = f"https://yande.re/tag.json?limit={limit}&order=count&name={tag}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        tags = Pykson().from_json(data, Tag)
        return tags
