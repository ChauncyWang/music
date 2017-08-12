from http import cookiejar

import requests

from music.api import BaseAPI


class XiamiAPI(BaseAPI):
    def __init__(self, timeout=60, proxy=None):
        self.session = requests.session()
        self.timeout = timeout
        self.proxies = {'http': proxy, 'https': proxy}
        self.session.cookies = cookiejar.LWPCookieJar('a.c')

    def search_artists(self, content, page, num):
        pass

    def search(self, content, t, page, num):
        pass

    def search_songs(self, content, page, num):
        pass

    def song_url(self, song):
        pass

    def get(self, url, params=None, headers=None, stream=False):
        resp = self.session.get(url, params=params, headers=headers, stream=stream)
        if 200 == resp.status_code:
            return resp

    def playable(self, song):
        pass

    def album_img_url(self, song):
        pass

    def lyric(self, song):
        pass

    def post(self, url, data=None, headers=None):
        pass
