# Assignment1
# Vicky Wang
# March 20, 2015


from pylab import *
import urllib2
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import requests

url_user = 'http://www.reddit.com/user/' + username + '/about.json'
header = {'user-agent': 'Vicky user-agent'}
user_json = requests.get(url_user, headers=header).json()
user_data = user_json['data']

is_mod = user_data['is_mod']
is_verified = user_data['has_verified_email']
is_gilded = user_data['is_gold']
author = user_data['name']
created_utc = user_data['created_utc']
link_karma = user_data['link_karma']
comment_karma = user_data['comment_karma']

url_comment = 'http://www.reddit.com/user/' + username + '/comments/json'
header = {'user-agent': 'Vicky user-agent'}
comment_json = requests.get(url_comment, headers=header).json()
comment_data = comment_json['data']

allcomments = comment_data['children']['data']
