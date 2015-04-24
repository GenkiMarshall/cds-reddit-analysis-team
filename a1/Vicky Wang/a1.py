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

'''url_user = 'http://www.reddit.com/user/' + username + '/about.json'
header = {'user-agent': 'Vicky user-agent'}
user_json = requests.get(url_user, headers=header).json()
user_data = user_json['data']'''

username = 'malleus__maleficarum'

def findData(url):
    header = {'user-agent': 'Vicky user-agent'}
    json = requests.get(url, headers=header).json()
    data = json['data']
    return data

user_data = findData('http://www.reddit.com/user/' + username + '/about.json')

is_mod = user_data['is_mod']
is_verified = user_data['has_verified_email']
is_gilded = user_data['is_gold']
author = user_data['name']
created_utc = user_data['created_utc']
link_karma = user_data['link_karma']
comment_karma = user_data['comment_karma']

url_comment_start = 'http://www.reddit.com/user/' + username + '/comments.json'
comment_data = findData(url_comment_start)

def getAllComment(comment_data):
    length = 0
    comment_children = comment_data['children']
    after = comment_data['after']
    if len(comment_children) < 25:
        length = length + len(comment_children)
        return length
    length = length + len(comment_children)
    print length
    url_comment_new = 'http://www.reddit.com/user/' + username + '/comments.json?count=25&after=' + after
    comment_data_new = findData(url_comment_new)
    length = length + getAllComment(comment_data_new)

print getAllComment(comment_data)

if getAllComment(comment_data) > 50:
    have_all_comments = False
else:
    have_all_comments = True
    
print have_all_comments
