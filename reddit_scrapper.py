import requests
import json
import os
import datetime
import time


posts_limit = 5
comments_limit = 30

subreddit = 'funny' # subreddit name
listing = 'top' #['hot', 'top', 'controvercial', 'new', rising]
timeframe = 'week'  #['hour', 'day', 'week', 'month', 'year, 'all']
best_comments = 5



# get reddit post
def request_subreddit_posts(subreddit, listing, limit, timeframe):
    url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
    request = requests.get(url,
                        headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36)'})
    return request.json()


# get posts and sort them by date, return the latest one.
def get_latest_post_id(reddit_data_json):
    sorted_posts_list = []
    posts = {}
    n = len(reddit_data_json['data']['children'])
    for i in range(n):
        post_time = reddit_data_json['data']['children'][i]['data']['created']
        post_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(post_time))
        post_id = reddit_data_json['data']['children'][i]['data']['id']
        posts[post_id] = post_time
    sorted_ids = dict(sorted(posts.items(), key=lambda item:item[1]))
    for key, value in sorted_ids.items():
        sorted_posts_list.append((key, value))
    return sorted_posts_list[n-1]


# get comments in a given post by using post id
def request_post_data(post_id, comments_limit):
    url = f'https://www.reddit.com/r/{subreddit}/comments/{post_id}.json?limit={comments_limit}'
    request = requests.get(url,
                        headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36)'})
    return request.json()


# get titles comments, images and video urls
def filter_post_data(reddit_data_json):
    age_restricted = reddit_data_json[0]['data']['children'][0]['data']['over_18']
    title, img_url, vid_url, audio_url, post_type, permalink = [],[],[],[],[],[]
    title.append(reddit_data_json[0]['data']['children'][0]['data']['title'])
    post_type.append(reddit_data_json[0]['data']['children'][0]['data']['post_hint'])
    if reddit_data_json[0]['data']['children'][0]['data']['media']:
        vid_url.append(reddit_data_json[0]['data']['children'][0]['data']['media']['reddit_video']['fallback_url'])
        audio_url.append('https://v.redd.it/' + vid_url[0].split('/')[3] + '/DASH_audio.mp4')
        img_url.append()
    else:
        img_url.append(reddit_data_json[0]['data']['children'][0]['data']['url'])

    return title, img_url, vid_url, audio_url, age_restricted#, post_type



# get 5 best comments under post
def filter_comments(post_comments_json):
    comment_list = []
    stickied = post_comments_json[1]['data']['children'][0]['data']['stickied']
    for i in range(0 + int(stickied), best_comments + int(stickied)):
        author = post_comments_json[1]['data']['children'][i]['data']['author']
        ups = post_comments_json[1]['data']['children'][i]['data']['ups']
        if author != '[deleted]':
            comment = post_comments_json[1]['data']['children'][i]['data']['body']
            comment_list.append(f'"{comment}" -by {author}, {ups} upvotes\n--------------')
    return comment_list



def get_the_best_post():
    comments_list = []
    data = request_subreddit_posts(subreddit, 'top', posts_limit, 'day')
    latest_id = get_latest_post_id(data)
    post_data = request_post_data(latest_id[0], comments_limit)
    media = filter_post_data(post_data)
    comments = filter_comments(post_data)
    for i in comments:
        comments_list.append(i)
    comments_list.append(f'https://www.reddit.com/r/{subreddit}/comments/{latest_id[0]}')
    return media, latest_id, comments_list

# print(get_the_best_post()[0])




# save reddit post json
def save_reddit_posts(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=True, indent=4)

def save_comments_json(comments_data):
    with open('comments.json', 'w') as f:
        json.dump(comments_data, f, ensure_ascii=True, indent=4)





# save temp video and audio files, then make combine them using ffmpeg, then remove temp files
def make_video(vid_url, audio_url):
    # define temp dir audio  and video files 
    script_dir = os.path.dirname(__file__)
    tmp_dir = os.path.abspath(os.path.join(script_dir, '.', '_tmp'))
    print(os.path.abspath(os.path.join(script_dir, '.', '_tmp')))
    os.makedirs(tmp_dir, mode=0o777, exist_ok=True)


    tmp_video_file = tmp_dir + '/' + 'out_video.mp4'
    tmp_audio_file = tmp_dir + '/' + 'out_audio.mp3'
    result_video = tmp_dir + '/' + 'result_video.mp4'

    with open(tmp_video_file, 'wb') as f:
        get = requests.get(vid_url, stream=True)
        f.write(get.content)

    with open(tmp_audio_file, 'wb') as f:
        get = requests.get(audio_url, stream=True)
        f.write(get.content)

    os.system(f'ffmpeg -y -i {tmp_video_file} -i {tmp_audio_file} -c copy {result_video}')
    os.remove(tmp_video_file)
    os.remove(tmp_audio_file)
    return result_video



