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

url = 'http://www.reddit.com/user/' + name + '/about.json'
header = {'user-agent': 'Vicky user-agent'}
r = requests.get(url, headers=header).json()
data = r['data']

is_mod = data['is_mod']
is_verified = data['has_verified_email']
is_gilded = data['is_gold']
author = data['name']
created_utc = data['created_utc']