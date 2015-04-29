# Assignment1
# Stephanie Wang
# April 17, 2015

import requests;

#input author's name
author = raw_input('Type a Reddit author\'s name')

# reddit requires user-agent for rate limiting
header = {'user-agent': 'Young user agent'}
# store author's json data
url = 'http://www.reddit.com/user/' + author + '/about.json'
response = requests.get(url, headers=header)
data = response.json()

