from flask import Flask
from flask import request
import requests
import time
import json
from dotenv import load_dotenv
import os
from threading import Thread
import reddit_scrapper as rs

app = Flask(__name__)

load_dotenv('.env')

token = os.environ.get('TOKEN')
tg_channel = os.environ.get('telegram_ch')
myChatId = int(os.environ.get('CHATID'))

update_frequecy = 25*60


URL = f'https://api.telegram.org/bot{token}/'
webhook_host = os.environ.get('HOST')


def send_images(chat_id, image_list, text=None, disable_notification=None):
    text = text.replace("'", "’")  # replace apostrophe with similar simbol ’, bug?
    photos = list(image_list)
    media = list()
    for count, photo in enumerate(photos):
        # print(photo)
        if count == 0:
            media.append({'type':'photo',
                          'media':photo,
                          'caption':text})
        else:
            media.append({'type':'photo',
                          'media':photo})
    # print('raw media = ',media)
    params = {
        'chat_id': chat_id,
        "media": str(media).replace("'", '"'),
        'disable_notification':disable_notification}
    request_url = URL + 'sendMediaGroup'
    r = requests.post(request_url, params)
    # print('params',params)
    print(r)
    if r.status_code == 200:
        return True
    else:
        return False



def send_video(chat_id, video=None, caption=None, disable_notification=None):
    url = URL+'sendVideo'
    answer = {'chat_id':chat_id,
                'video':video,
                'caption':caption,
                'disable_notification':disable_notification}
    r = requests.post(url, json=answer)
    return r.json()


def send_message(chat_id, text=None, disable_notification=None):
    url = URL+'sendMessage'
    answer = {'chat_id':chat_id,
                'text':text,
                'disable_notification':disable_notification}
    r = requests.post(url, json=answer)
    # print(r.json())
    return r.json()


def get_updates():
    url = URL+'getUpdates'
    r = requests.get(url)
    # print(r.json())
    # write_json(r.json())
    return(r.json())


def set_webhook(webhook_host_url):
     url = URL + 'setWebhook?url=' + webhook_host_url
     r = requests.get(url)
     print(r.json()['description'])
     return(r.json())


def delete_webhook():
    url = URL+'deleteWebhook'
    r = requests.get(url)
    print(r.json()['description'])
    return(r.json())


def get_channel_post():
    r = request.get_json()
    channel_message = r['channel_post']['text']
    channel_id = r['channel_post']['sender_char']['id']
    return channel_message, channel_id



# def check_for_new_post(twitter_account, telegram_channel):
#     twt_data, old_id, new_id, picture_list, video_list, gifs = ([] for i in range(6))
#     # print('making initial tweeter request...')
#     reddit_data = rs.get_the_best_post()
#     old_id = reddit_data[1][0]
#     title = reddit_data[0][0][0]
#     comments = reddit_data[2]
#     picture_list = reddit_data[2]
#     video_list = reddit_data[3]
#     gifs = reddit_data[4]
#     # print('tweet data =', twt_data)
#     while True:
#         # print('extra thread executed!')
#         time.sleep(update_frequecy)
#         updated_twt_data = get_tweet(twitter_account)
#         new_id = updated_twt_data[0]
#         print('runnning on ' ,twitter_account)
#         print('tweet data updated!')
#         if new_id != old_id:
#             picture_list.clear()
#             video_list.clear()
#             # gifs.clear()
#             tweet = updated_twt_data[1]
#             picture_list = updated_twt_data[2]
#             video_list = updated_twt_data[3]
#             gifs = updated_twt_data[4]
#             print('There is a new post with id ', new_id, 'tweet =', tweet,'has links =', picture_list, video_list, gifs, '\n')
#             old_id = new_id
#             twt_data.clear()
#             twt_data = [new_id, tweet, picture_list, video_list, gifs]
#             send_new_tg_message(twt_data, telegram_channel, disable_notification=True)
#             # print('thread lock released! \n')

#         else:
#             print('No new tweets! Old id is ', old_id, 'tweet =', tweet, 'has links =', picture_list, video_list, gifs, '\n')
#             # print('thread lock released! \n')
#             # pass # do nothing








# def send_new_tg_message(twt_data, channel_id, disable_notification=None):
#     new_id = twt_data[0]
#     tweet = twt_data[1]
#     picture_list = twt_data[2]
#     video_list = twt_data[3]
#     gifs = twt_data[4]
#     for item, (pictures, vids, gif) in enumerate(zip(picture_list, video_list, gifs)):
#         # print(item, pictures, vids, gif)
#         if vids:
#             for video in vids:
#                 # print(video)
#                 try:
#                     send_video(channel_id, video, tweet, disable_notification)
#                     print('video sent!', new_id, tweet, video, '\n')
#                 except:
#                     print('ERROR: wrong video format', item, video, tweet, '\n')
#         elif pictures:
#             send_images(channel_id, pictures, tweet, disable_notification)
#             # send_photo(channel_id, pictures, tweet)
#             print('pictures sent!', pictures, '\n')
#         elif gif:
#             send_video(channel_id, gif[0], tweet, disable_notification)
#             print('gif sent!\n')
#         else:
#             send_message(channel_id, tweet, disable_notification)
#             print(new_id, tweet, 'Tweet sent, there are NO pictures, videos or gifs \n')






@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        if 'message' in r:
            chat_id = r['message']['chat']['id']
            msg = r['message']['text']
            print('received a private message', msg)
            if '/start' in msg:
                if int(chat_id) == int(myChatId):
                    send_message(chat_id, 'working!', disable_notification=True)
                else:
                    send_message(chat_id, "you're not allowed to use this bot! 🤨")
        elif 'channel_post' in r:
            print('received a channel message')
    return '<h1>200<h1>'



d={}

for i in zip(twt_list, ch_list):
    d[i[0]] = i[1]


def run_threads(dct):
    threads = []
    for k, v in dct.items():
        threads.append(Thread(target=check_for_new_post, args=[k, v], daemon=True))
    for thread in threads:
        thread.start()
        print('running thread',thread.getName(), '\n')
    # for thread in threads:
    #     thread.join()


delete_webhook()
set_webhook(webhook_host)

run_threads(d)

print('main thread execution...')




if __name__ == '__main__':
    app.run()
