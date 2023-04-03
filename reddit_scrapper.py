import requests
import json
import os
import datetime
import time


posts_limit = 5
comments_limit = 30
best_comments = 3
video_quality = 35 # less is more

test_subreddit = 'memes' # subreddit name
test_listing = 'new' #['hot', 'top', 'controvercial', 'new', rising]
test_timeframe = 'day'  #['hour', 'day', 'week', 'month', 'year, 'all']



# get reddit post
def request_subreddit_posts(subreddit, listing, posts_limit, timeframe):
    url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={posts_limit}&t={timeframe}'
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
        post_id = reddit_data_json['data']['children'][i]['data']['id']  # get id 
        posts[post_id] = post_time  # add key and value to dictionar "posts"
    sorted_ids = dict(sorted(posts.items(), key=lambda item:item[1]))
    for key, value in sorted_ids.items():
        sorted_posts_list.append((key, value))
    return sorted_posts_list[n-1]



# get comments in a given post by using post id
def request_post_data(subreddit, post_id, comments_limit):
    url = f'https://www.reddit.com/r/{subreddit}/comments/{post_id}.json?limit={comments_limit}'
    request = requests.get(url,
                        headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36)'})
    return request.json()


# get titles comments, images and video urls
def filter_post_data(reddit_data_json):
    age_restricted = reddit_data_json[0]['data']['children'][0]['data']['over_18']
    title, img_url, vid_url, audio_url, post_type, permalink = [],[],[],[],[],[]
    title.append(reddit_data_json[0]['data']['children'][0]['data']['title'])
    # post_hint types = "hosted:video", "image", None, "rich:video", "link"
    # post_type.append(reddit_data_json[0]['data']['children'][0]['data']['post_hint'])
    try:
        vid_url.append(reddit_data_json[0]['data']['children'][0]['data']['media']['reddit_video']['fallback_url'])
        audio_url.append('https://v.redd.it/' + vid_url[0].split('/')[3] + '/DASH_audio.mp4')
        img_url.append(None)
    except TypeError as e:
        print(e, 'no video found')
    try:
        x = reddit_data_json[0]['data']['children'][0]['data']['gallery_data']['items']
        y = reddit_data_json[0]['data']['children'][0]['data']['media_metadata']
        for i in range(len(x)):
            med_id  = x[i]['media_id']
            temp_link = y[med_id]['s']['u']
            temp_link = temp_link.replace("amp;", '')
            img_url.append(temp_link)
    except KeyError as e:
        print(e, 'no galery found')
        pass
    if not img_url:
        img_url.append(reddit_data_json[0]['data']['children'][0]['data']['url'])

    return title, img_url, vid_url, audio_url, age_restricted#, post_type



# get 5 best comments under post
def filter_comments(post_comments_json):
    comment_list = []
    if post_comments_json[1]['data']['children']:
        stickied = post_comments_json[1]['data']['children'][0]['data']['stickied']
        if len(post_comments_json[1]['data']['children']) > best_comments:
            for i in range(0 + int(stickied), best_comments + int(stickied)):
                author = post_comments_json[1]['data']['children'][i]['data']['author']
                ups = post_comments_json[1]['data']['children'][i]['data']['ups']
                if author != '[deleted]':
                    comment = post_comments_json[1]['data']['children'][i]['data']['body']
                    comment_list.append(f'"{comment}" -by {author}, {ups} upvotes\n--------------')
    return comment_list



def get_the_best_post(subreddit):
    reddit_data = []
    comments_list = []
    data = request_subreddit_posts(subreddit, test_listing, posts_limit, test_timeframe)
    latest_id = get_latest_post_id(data)
    print(f'id is {latest_id}\n \n')
    post_data = request_post_data(subreddit, latest_id[0], comments_limit)
    # print(post_data)
    media = filter_post_data(post_data)
    print(f'media:{media}\n')
    comments = filter_comments(post_data)
    print(f'media:{comments}\n')
    for i in comments:
        comments_list.append(i)
    comments_list.append(f'https://www.reddit.com/r/{subreddit}/comments/{latest_id[0]}')
    reddit_data.append(media)
    reddit_data.append(latest_id)
    reddit_data.append(comments_list)
    return reddit_data

# d = get_the_best_post()
# source_link = d[2][-1]
# comments = d[2][:-1]

# print(comments)
# print(d, '\n','\n')
# l = d[:-1]
# print(l)



# save reddit post json
def save_reddit_posts(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=True, indent=4)

def save_comments_json(comments_data):
    with open('comments.json', 'w') as f:
        json.dump(comments_data, f, ensure_ascii=True, indent=4)



# save temp video and audio files, then make combine them using ffmpeg, then remove temp files
def make_video(vid_url, audio_url):
    has_audio = True
    # define temp dir audio  and video files 
    script_dir = os.path.dirname(__file__)
    tmp_dir = os.path.abspath(os.path.join(script_dir, '.', '_tmp'))
    # print(os.path.abspath(os.path.join(script_dir, '.', '_tmp')))
    os.makedirs(tmp_dir, mode=0o777, exist_ok=True)

    tmp_video_file = tmp_dir + '\\' + 'out_video.mp4'
    tmp_audio_file = tmp_dir + '\\' + 'out_audio.mp3'
    result_video = tmp_dir + '\\' + 'result_video.mp4'

    with open(tmp_video_file, 'wb') as f:
        r = requests.get(vid_url, stream=True)
        f.write(r.content)

    with open(tmp_audio_file, 'wb') as f:
        r = requests.get(audio_url, stream=True)
        size = int(r.headers['Content-Length'])
        print(f'audio size is {size} bites')
        if size < 1024:
            print(f'video has no audio; audio size is {size} bytes')
            has_audio = False
        f.write(r.content)

    print('encoding started...')
    print('video has audio?', has_audio)


    # check if video has audio, if it doesnt encode only video. Encoding done with h265
    start = time.time()
    if has_audio:
        print('encoding video with audio')
        os.system(f'ffmpeg -y -i {tmp_video_file} -i {tmp_audio_file} -vcodec libx265 -crf {video_quality} {result_video} -loglevel error')
    else:
        os.system(f'ffmpeg -y -i {tmp_video_file} -vcodec libx265 -crf {video_quality} {result_video}')
        print('video has no audio')
        # result_video = tmp_video_file
    
    # os.remove(tmp_video_file)
    # os.remove(tmp_audio_file)
    print(f'encoding complete, temp files cleaned... encoded video is {result_video}')
    print('encoding time', time.time() - start)
    return result_video





v2 = ['https://v.redd.it/ymbka65obbqa1/DASH_480.mp4?source=fallback']
a2 = ['https://v.redd.it/ymbka65obbqa1/DASH_audio.mp4']

v = ['https://v.redd.it/njsk41ake4w31/DASH_1080?source=fallback']
# print('audio url =', 'https://v.redd.it/' + v[0].split('/')[3] + '/DASH_audio.mp4')
a = ['https://v.redd.it/njsk41ake4w31/DASH_audio.mp4']

v3 = ['https://v.redd.it/v3s462zrqaqa1/DASH_1080.mp4?source=fallback']
a3 = ['https://v.redd.it/v3s462zrqaqa1/DASH_audio.mp4']

# print(a)
# make_video(v3[0], a3[0])





def get_post_info_dev(reddit_data_json):
    post_date, ups, titles, link, post_id = [], [], [], [], []
    n = len(reddit_data_json['data']['children'])
    for i in range(n):
        post_time = reddit_data_json['data']['children'][i]['data']['created']
        post_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(post_time))
        post_date.append(post_time)
        ups.append(reddit_data_json['data']['children'][i]['data']['ups'])
        titles.append(reddit_data_json['data']['children'][i]['data']['title'])
        link.append('https://www.reddit.com'+reddit_data_json['data']['children'][i]['data']['permalink'])
        post_id.append(reddit_data_json['data']['children'][i]['data']['id'])

    return post_date, ups, link, titles, post_id




# posts = request_subreddit_posts('funny', 'top', 15, 'day')

# info = get_post_info(posts)

# print(info)

# ups = posts['data']['children'][1]['data']['ups']

# print(ups)





##  test multiple images in 1 post
# test = requests.get('https://www.reddit.com/r/commandandconquer/comments/125eg9m/.json?limit=15',headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36)'})

# test = test.json()


# res = filter_post_data(test)[1]

# for i in res:
#     print(i)
