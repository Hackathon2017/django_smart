#!/usr/bin/env python
import os
import sys
 
import requests, json  

datas = json.dumps({
        "id": 3,
        "name": "Hechmi hamdi",
        "geocode": "36.808314, 10.183735",
        "about_website": "no web site",
        "phone": "71 455233",
        "speciality": 2 
        })
 
headers = {'content-type': 'application/json'}
response = requests.post("http://172.16.3.223:8000/specialists/", data=datas, headers=headers)
print("response: ", response.text)