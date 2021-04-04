from urllib.parse import urlparse, parse_qsl

class Params:
    def __init__(self, url: str):
        self.authkey_querys={}
        parsed = urlparse(url)
        querys = dict(parse_qsl(parsed.query))
        self.authkey_querys = {"authkey_ver": "1", "authkey": querys["authkey"], "lang": "zh-cn", "end_id": ""}

    def size(self, size):
        self.authkey_querys["size"] = size
        return self

    def gacha_type(self, gacha_type):
        self.authkey_querys["gacha_type"] = gacha_type
        return self

    def page(self, page):
        self.authkey_querys["page"] = page
        return self

    def end_id(self, end_id):
        self.authkey_querys["end_id"] = end_id
        return self

    def get(self):
        return self.authkey_querys
