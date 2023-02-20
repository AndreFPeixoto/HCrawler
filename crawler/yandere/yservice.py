import requests
from pykson import Pykson
from .models.Tag import Tag
from .models.Post import Post
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

    @staticmethod
    def get_posts_with_tag_by_page(tag, page):
        url = f"https://yande.re/post.xml?limit=40&page={page}&tags={tag}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        root = ET.fromstring(response.text)
        offset = int(root.attrib['offset'])
        posts = []
        for child in root:
            post_attributes = child.attrib
            post = Pykson().from_json(post_attributes, Post, accept_unknown=True)
            posts.append(post)
        return posts
