import requests
import json
import os

limit = 14
comments_limit = 10


timeframe = 'week'  #['hour', 'day', 'week', 'month', 'year, 'all']

listing = 'top' #['hot', 'top', 'controvercial', 'new', rising]

test_post = f'https://www.reddit.com/r/funny/comments/11qhab2/my_hometown_just_unveiled_a_911_memorial_at_the/.json?limit={comments_limit}'


'https://www.reddit.com/r/funny/comments/11qhab2/my_hometown_just_unveiled_a_911_memorial_at_the/.json?'

subreddit = 'funny' # subreddit name

try:
    base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
except:
    print("can't make a request")


def make_request(url):
    request = requests.get(url,
                        headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36)'})
    return request.json()


reddit_post = make_request(base_url)
post_comments = make_request(test_post)

# save reddit post json
# with open('data.json', 'w') as f:
#     json.dump(base_url, f, ensure_ascii=True, indent=4)


# with open('comments.json', 'w') as f:
#     json.dump(post_comments, f, ensure_ascii=True, indent=4)



# get titles comments, images and video urls
# title = reddit_post['data']['children'][12]['data']['title']
# img_url = reddit_post['data']['children'][12]['data']['url']
# vid_url = reddit_post['data']['children'][12]['data']['media']['reddit_video']['fallback_url']
# audio_url = 'https://v.redd.it/' + vid_url.split('/')[3] + '/DASH_audio.mp4'

# post_type = reddit_post['data']['children'][12]['data']['post_hint']
permalink = reddit_post['data']['children'][12]['data']['permalink']

comments = f'https://www.reddit.com/{permalink}.json?'


# comment = post_comments[1]['data']['children'][1]['data']['body']
# author = post_comments[1]['data']['children'][1]['data']['author']
# ups = post_comments[1]['data']['children'][1]['data']['ups']

print('Here are some of the funny comments, enjoy:')
for i in range(1,8):
    comment = post_comments[1]['data']['children'][i]['data']['body']
    author = post_comments[1]['data']['children'][i]['data']['author']
    ups = post_comments[1]['data']['children'][i]['data']['ups']

    print(f'"{comment}" -by {author}, {ups} upvotes')





# print(title, '\n', img_url, '\n', vid_url,'\n', audio_url,'\n', post_type)

# if post_type == 'hosted:video':
#     print('there is a video!')



# # define temp dir audio  and video files 
# script_dir = os.path.dirname(__file__)
# tmp_dir = os.path.abspath(os.path.join(script_dir, '.', '_tmp'))
# print(os.path.abspath(os.path.join(script_dir, '.', '_tmp')))
# os.makedirs(tmp_dir, mode=0o777, exist_ok=True)


# tmp_video_file = tmp_dir + '/' + 'out_video.mp4'
# tmp_audio_file = tmp_dir + '/' + 'out_audio.mp3'
# result_video = tmp_dir + '/' + 'result_video.mp4'


# print(tmp_video_file, tmp_audio_file, result_video)


# # save temp video and audio files, then make combine them using ffmpeg, then remove temp files
# def make_video(vid_url, audio_url):
#     with open(tmp_video_file, 'wb') as f:
#         get = requests.get(vid_url, stream=True)
#         f.write(get.content)

#     with open(tmp_audio_file, 'wb') as f:
#         get = requests.get(audio_url, stream=True)
#         f.write(get.content)

#     os.system(f'ffmpeg -y -i {tmp_video_file} -i {tmp_audio_file} -c copy {result_video}')
#     os.remove(tmp_video_file)
#     os.remove(tmp_audio_file)



