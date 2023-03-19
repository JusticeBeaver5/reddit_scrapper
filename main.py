from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import requests
import tweepy
import re
import time
import json
from dotenv import load_dotenv
import os
from threading import Thread


app = Flask(__name__)




if __name__ == '__main__':
    app.run()
