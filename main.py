from flask import Flask
from flask import request
import requests
import time
import json
from dotenv import load_dotenv
import os
from threading import Thread
import reddit_scrapper as rs
import file_handler as fh

app = Flask(__name__)

load_dotenv('.env')

token = os.environ.get('TOKEN')
tg_channel = os.environ.get('TG_CHANNEL')
myChatId = int(os.environ.get('CHATID'))
subreddits = os.environ.get('SUBREDDITTS').split(',')

update_frequecy = 1*60*60


URL = f'https://api.telegram.org/bot{token}/'
webhook_host = os.environ.get('HOST')

silent = True


# *[source](http://www.example.com/)*&parse_mode=MarkdownV2

def send_message(chat_id, text, parse_mode=None, entities=None, disable_web_page_preview=None, disable_notification=None):
    url = URL+'sendMessage'
    answer = {'chat_id':chat_id,
                'text':text,
                'parse_mode':parse_mode,
                'entities':entities,
                'disable_web_page_preview':disable_web_page_preview,
                'disable_notification':disable_notification}
    r = requests.post(url, json=answer)
    # print(r.json())
    return r.json()



def send_images_new(chat_id, image_list, text=None, parse_mode=None, disable_web_page_preview=None, disable_notification=None):
    # text = text.replace("'", "’")  # replace apostrophe with similar simbol ’, bug?
    photos = list(image_list)
    media = list()
    for count, photo in enumerate(photos):
        # print(photo)
        if count == 0:
            media.append({"type":"photo",
                          "media":photo,
                          "caption":text,
                          "parse_mode":parse_mode})
        else:
            media.append({"type":"photo",
                          "media":photo})
    # print('raw media = ',media)
    answer = {
        "chat_id": chat_id,
        "media": media,
        "disable_web_page_preview":disable_web_page_preview,
        "disable_notification":disable_notification}
    request_url = URL + "sendMediaGroup"
    r = requests.post(request_url, json=answer)
    # print(r.json())
    return r.json()



def send_video(chat_id, video=None, caption=None, parse_mode=None, disable_web_page_preview=None, disable_notification=None):
    url = URL+'sendVideo'
    answer = {'chat_id':chat_id,
                'video':video,
                'caption':caption,
                'parse_mode':parse_mode,
                'disable_web_page_preview':disable_web_page_preview,
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



def check_for_new_post(subreddit, telegram_channel):
    reddit_data, old_id, new_id, picture_list, video_list = ([] for i in range(5))
    reddit_data = rs.get_the_best_post(subreddit)
    print('reddit data:',reddit_data)
    old_id = reddit_data[1][0]
    # reddit_data = rs.get_the_best_post(subreddit)
    # send_new_tg_message(reddit_data, telegram_channel, silent)
    while True:
        time.sleep(update_frequecy)
        print(f'checking {subreddit}')
        updated_reddit_data = rs.get_the_best_post(subreddit)
        new_id = updated_reddit_data[1][0]
        print(new_id)
        # print('runnning on ' ,)
        print('reddit data updated!')
        if new_id != old_id:
            # post_title = updated_reddit_data[0][0][0]
            # picture_list = updated_reddit_data[0][1]
            # video_list = updated_reddit_data[0][2]
            # audio_list = updated_reddit_data[0][3]
            # print(post_title, picture_list, video_list, audio_list)
            # print('There is a new post with id ', new_id, 'post_title =', post_title,'has links =', picture_list, video_list, '\n')
            # old_id = new_id
            reddit_data.clear()
            reddit_data = updated_reddit_data
            send_new_tg_message(reddit_data, telegram_channel, silent)
        else:
            print('No new tweets! Old id is ', old_id, '\n')




table = str.maketrans({"-":r"\-", "]":r"\]",
                       "[":r"\]", "?":r"\?",
                       "\\":r"\\", "^":r"\^", 
                       "$":r"\$", "*":r"\*", 
                       ".":r"\.", "'":r"\'", 
                       "&":r"\&", "_":r"\_",
                       ",":r"\,", "!":r"\!",
                       "(":r"\(", ")":r"\)"})


def send_new_tg_message(reddit_data, channel_id, silent):
    print('executing function!!')
    # if not reddit_data:
    #     reddit_data = rs.get_the_best_post(subreddit)
    print(f'updated data: {reddit_data}')
    new_id = reddit_data[1][0]
    post_title = reddit_data[0][0][0]
    picture_list = reddit_data[0][1]
    video_list = reddit_data[0][2]
    audio_list = reddit_data[0][3]
    source_link = reddit_data[2][-1]
    comments = reddit_data[2][:-1]
    comments = '\n'.join(comments)
    subreddit = reddit_data[0][-1]

    message = comments.translate(table)
    post_title = post_title.translate(table)

    print(f'source: {source_link}')
    # print(post_title)
    # print(picture_list)
    # print(comments)
    print('total number of characters =', int(len(message)) + int(len(post_title)) + int(len(source_link)))


    # print(post_title)
    # print(picture_list)
    print('video', video_list)
    print('audio', audio_list)
    # print(comments)
    

    if video_list:
        try:
            mp4_video = rs.make_video(video_list[0], audio_list[0])
            mp4_video = fh.upload_file(mp4_video)
            send_video(channel_id, mp4_video, f'*{post_title}*\n\nHere are some top comments:\n\n{message}\n[*source \\- {subreddit}*]({source_link})', parse_mode='MarkdownV2', disable_web_page_preview=True, disable_notification=silent)
            print('video sent!', new_id, post_title, video_list, '\n')
        except:
            print('ERROR: could not send video', video_list, source_link, '\n')

    elif picture_list[0][-4:] == '.gif':
        send_video(channel_id, picture_list[0], f'*{post_title}*\n\nHere are some top comments:\n\n{message}\n[*source \\- {subreddit}*]({source_link})', parse_mode='MarkdownV2', disable_web_page_preview=True, disable_notification=silent)
        
    elif picture_list[0][-4:] == '.jpg' or picture_list[0][-5:] == '.jpeg' or picture_list[0][-4:] == '.png':
        send_images_new(channel_id, picture_list, f'*{post_title}*\n\nHere are some top comments:\n\n{message}\n[*source \\- {subreddit}*]({source_link})', parse_mode='MarkdownV2', disable_web_page_preview=True, disable_notification=silent)
        print('pictures sent!', picture_list, '\n')

    else:
        send_message(channel_id, f'*{post_title}*\n\nHere are some top comments:\n\n{message}\n[*source \\- {subreddit}*]({source_link})', parse_mode='MarkdownV2', disable_web_page_preview=True, disable_notification=silent)
        print(new_id, post_title, 'post_title sent, there are NO pictures, videos or gifs \n')




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
                    send_message(chat_id, '*working*', parse_mode='MarkdownV2', disable_notification=silent)
                else:
                    send_message(chat_id, "you're not allowed to use this bot! 🤨")
        elif 'channel_post' in r:
            print('received a channel message')
    return '<h1>200<h1>'



d=[]

for item in subreddits:
    print(f'executing following subreddits: "{item}"')
    d.append(item)


def run_threads(lst):
    threads = []
    for item in lst:
        threads.append(Thread(target=check_for_new_post, args=[item, tg_channel], daemon=True))
    for thread in threads:
        thread.start()
        print('running thread',thread.getName(), '\n')
    # for thread in threads:
    #     thread.join()


delete_webhook()
set_webhook(webhook_host)

print('main thread execution...')

run_threads(d)


if __name__ == '__main__':
    app.run()