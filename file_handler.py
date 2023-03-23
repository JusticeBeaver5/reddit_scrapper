import requests
import json


def upload_file(file):
    uguu_url = 'https://uguu.se/upload.php'

    with open(file, 'rb') as f:
        files = {'files[]': f,}
        print(files)
        response = requests.post(uguu_url, files=files)
    
    print(response.json())
    return response.json()['files'][0]['url']



# video_file = 'D:\\python\\reddit_scrapper_tg_bot\\_tmp\\result_video.mp4'

# upload_file(video_file)