import requests
from pykson import Pykson
from .models.Tag import Tag
import xml.etree.ElementTree as ET


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

    @staticmethod
    def get_posts_count_offset(tag):
        url = f"https://yande.re/post.xml?limit=1&tags={tag}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        root = ET.fromstring(response.text)
        return root.attrib
