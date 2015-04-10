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
# not is_link => comment
def get_data (url, is_link) :
    data = requests.get(url, headers=header).json()
    i = 0 if is_link else 1
    meta_data = data[i]['data']['children'][0]['data']

    # starting from top

    # starting from bottom

    print(is_link, meta_data)

get_data(link_ex, True)
time.sleep(2)
get_data(comment_ex, False)
