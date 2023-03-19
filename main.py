from flask import Flask
from flask import request
from flask import jsonify
import requests
import time
import json
from dotenv import load_dotenv
import os
from threading import Thread

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


delete_webhook()
set_webhook(webhook_host)

worker1 = Thread(target=check_for_new_post, daemon=True)
worker1.start()
print('main thread execution...')

if __name__ == '__main__':
    app.run()
