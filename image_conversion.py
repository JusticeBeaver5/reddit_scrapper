import requests
import os
from dotenv import load_dotenv

load_dotenv('.env')

key = os.environ.get('filestack_key')



img_a = 'https://i.redd.it/4yu6l24va9i61.jpg'
img_b = 'https://i.redd.it/h1jjb7aeq6qa1.jpg'


url = f'https://cdn.filestackcontent.com/{key}/output=format:jpg,quality:50/{img_b}'




r = requests.get(url, stream=True)
if r.status_code == 200:
    with open('text_image.jpg', 'wb') as f:
        for chunk in r:
            f.write(chunk)