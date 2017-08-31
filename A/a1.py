import json
import base64
import os

import requests

for a in os.listdir("网纹照"):
    a = "网纹照/" + a
    file = open(a, 'rb').read()
    img = base64.b64encode(file).decode()
    url = "http://192.168.199.145:8080/huiyi/deshpic"
    header = {
        "User-Agent":" Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Content-type":"application/json",
    }
    print(img)
    data = {
        "type": "PDP001",
        "img": img
    }
    data = json.dumps(data)
    resp = requests.post(url,data=data,headers=header)
    code = resp.status_code
    if code == 200:
        msg = json.loads(resp.text)['message'].encode()
        msg = base64.b64decode(msg)
    else:
        print(code)
        print(resp.content)