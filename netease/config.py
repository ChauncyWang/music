import os

# ras 加密参数
modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68" \
          "ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee3" \
          "41f56135fccf695280104e0312ecbda92557c93870114af6c9d" \
          "05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3" \
          "e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
nonce = "0CoJUm6Qyw8W8jud"
pub_key = "010001"

# api 相关 url
search_url = "http://music.163.com/weapi/cloudsearch/get/web?csrf_token="
song_url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
lyric_url = 'http://music.163.com/api/song/lyric'
toplist_url = 'http://music.163.com/discover/toplist'

header = {
    "Host": "music.163.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
}
r = os.environ['HOME']
root_path = '%s/ChavaMusic/' % r
cookie_path = root_path + 'cookie'
cache_path = root_path + 'cache/'

if not os.path.exists(root_path):
    os.mkdir(root_path)

if not os.path.exists(cache_path):
    os.mkdir(cache_path)
