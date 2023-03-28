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


def get_image_size(url):
    r = requests.head(url)
    size = r.headers['Content-Length']
    # print(round(int(size)/(1024*1024), ndigits=4),'mb')
    return round(int(size)/(1024*1024), ndigits=4)





# ''' tests'''

# video_file = 'D:\\python\\reddit_scrapper_tg_bot\\_tmp\\result_video.mp4'
# upload_file(video_file)

# img_urls = ['https://i.redd.it/h1jjb7aeq6qa1.jpg', 'https://i.redd.it/4yu6l24va9i61.jpg']

# print([get_image_size(i) for i in img_urls])


# upload_file(img_urls[1])