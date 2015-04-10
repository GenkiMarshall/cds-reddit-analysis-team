#! /bin/python2

import time
import requests

# DOCS : see A1 excel sheet for now

# reddit requires user-agent for rate limiting
header = {'user-agent': 'part two user agent'}

base_ex = "https://www.reddit.com/r/pics/comments/324ln7/a_giant_boulder_fell_on_the_highway_in_ohio"
link_ex = base_ex + ".json"
comment_ex = base_ex + "/cq7t7ka.json"

def get_data (url) :

    r = requests.get(url, headers=header)
    data = r.json()[0]['data']['children'][0]['data']

    print(data)

get_data(link_ex)
time.sleep(2)
get_data(comment_ex)
