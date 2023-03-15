import requests
import json
import os

limit = 14

timeframe = 'day'  #['hour', 'day', 'week', 'month', 'year, 'all']

listing = 'hot' #['hot', 'top', 'controvercial', 'new', rising]


subreddit = 'funny' # subreddit name

try:
    base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
except:
    print("can't make a request")

request = requests.get(base_url,
                       headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36)'})

data = request.json()

with open('data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=True, indent=4)

title = data['data']['children'][12]['data']['title']
img_url = data['data']['children'][12]['data']['url']
vid_url = data['data']['children'][12]['data']['media']['reddit_video']['fallback_url']
audio_url = 'https://v.redd.it/' + vid_url.split('/')[3] + '/DASH_audio.mp4'

print(title, '\n', img_url, '\n', vid_url,'\n', audio_url)

script_dir = os.path.dirname(__file__)
tmp_dir = os.path.abspath(os.path.join(script_dir, '.', '_tmp'))
print(os.path.abspath(os.path.join(script_dir, '.', '_tmp')))
os.makedirs(tmp_dir, mode=0o777, exist_ok=True)

tmp_video_file = tmp_dir + '/' + 'out_video.mp4'
tmp_audio_file = tmp_dir + '/' + 'out_audio.mp3'
result_video = tmp_dir + '/' + 'result_video.mp4'

print(tmp_video_file, tmp_audio_file, result_video)

with open(tmp_video_file, 'wb') as f:
    get = requests.get(vid_url, stream=True)
    f.write(get.content)

with open(tmp_audio_file, 'wb') as f:
    get = requests.get(audio_url, stream=True)
    f.write(get.content)

os.system(f'ffmpeg -y -i {tmp_video_file} -i {tmp_audio_file} -c copy {result_video}')
os.remove(tmp_video_file)
os.remove(tmp_audio_file)



