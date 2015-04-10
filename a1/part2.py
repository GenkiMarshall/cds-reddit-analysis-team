#! /bin/python2

import time
import requests

# DOCS : see A1 excel sheet for now

# reddit requires user-agent for rate limiting
header = {'user-agent': 'part two user agent'}

base_ex = "https://www.reddit.com/r/pics/comments/324ln7/a_giant_boulder_fell_on_the_highway_in_ohio"
link_ex = base_ex + ".json"
comment_ex = base_ex + "/cq7t7ka.json"

# HELPERS

# MAIN
def get_data (url) :

    r = requests.get(url, headers=header)
    data = r.json()

    meta_data = data[0]['data']['children'][0]['data']
    other_data = data[1]['data']['children']

    # starting from top

    # starting from bottom

    print(meta_data)
    print(other_data)

get_data(link_ex)
time.sleep(2)
get_data(comment_ex)
