import requests
import json
import os

limit = 14
comments_limit = 30

subreddit = 'funny' # subreddit name
listing = 'top' #['hot', 'top', 'controvercial', 'new', rising]
timeframe = 'week'  #['hour', 'day', 'week', 'month', 'year, 'all']

test_post = f'https://www.reddit.com/r/funny/comments/11svz0o/i_made_a_song_entirely_of_artists_singing_yeah/.json?limit={comments_limit}'

base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'



def make_request(url):
    request = requests.get(url,
                        headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36)'})
    return request.json()


# get reddit post
def request_reddit_data(subreddit, listing, limit, timeframe):
    url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
    request = requests.get(url,
                        headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36)'})
    return request.json()


# get titles comments, images and video urls
def filter_reddit_data(reddit_data_json):
    # title, img_url, vid_url, audio_url, post_type, permalink = [],[],[],[],[],[]
    title = reddit_data_json['data']['children'][0]['data']['title']
    img_url = reddit_data_json['data']['children'][0]['data']['url']
    # vid_url.append(reddit_data_json['data']['children'][0]['data']['media']['reddit_video']['fallback_url'])
    # audio_url.append('https://v.redd.it/' + vid_url.split('/')[3] + '/DASH_audio.mp4')
    post_type = reddit_data_json['data']['children'][0]['data']['post_hint']
    permalink = reddit_data_json['data']['children'][0]['data']['permalink']

    return title, img_url, post_type, permalink


# get comments in a given post
def get_comments(permalink, comments_limit):
    url = f'https://www.reddit.com{permalink}.json?limit={comments_limit}'
    request = requests.get(url,
                        headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36)'})
    return request.json()


# get 5 best comments under post
def filter_comments(post_comments_json):
    comment_list = []
    stickied = post_comments_json[1]['data']['children'][0]['data']['stickied']
    for i in range(0 + int(stickied), 5 + int(stickied)):
        author = post_comments_json[1]['data']['children'][i]['data']['author']
        ups = post_comments_json[1]['data']['children'][i]['data']['ups']
        if author != '[deleted]':
            comment = post_comments_json[1]['data']['children'][i]['data']['body']
            comment_list.append(f'--------------\n"{comment}" -by {author}, {ups} upvotes')
    return comment_list


reddit_post = request_reddit_data('funny', 'top', 1, 'day')
data = filter_reddit_data(reddit_post)
post_comments = get_comments(data[3], 10)
x = filter_comments(post_comments)

print('And here are some of the funny comments, enjoy:')

for i in x:
    print(i)

print(f'source https://www.reddit.com{data[3]}')





# save reddit post json
# with open('data.json', 'w') as f:
#     json.dump(base_url, f, ensure_ascii=True, indent=4)

# with open('comments.json', 'w') as f:
#     json.dump(post_comments, f, ensure_ascii=True, indent=4)



# print(title, '\n', img_url, '\n', vid_url,'\n', audio_url,'\n', post_type)

# if post_type == 'hosted:video':
#     print('there is a video!')






# print(tmp_video_file, tmp_audio_file, result_video)


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



