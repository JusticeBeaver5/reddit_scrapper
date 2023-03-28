import requests
import json
import os
from dotenv import load_dotenv

load_dotenv('.env')


api_key = os.environ.get('IMG_BB')

url = 'https://api.imgbb.com/1/upload'


def upload_to_img_bb(img_url):
    params = {
        'expiration': 600,
        'key':api_key
        }
    files = {
        'image':(None, img_url)
    }
    r = requests.post(url, params=params, files=files)
    return r.json()



img_b = 'https://i.redd.it/h1jjb7aeq6qa1.jpg'

print(upload_to_img_bb(img_b))