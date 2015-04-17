#! /bin/python2

import time
import requests

# -- api notes --
# https://www.reddit.com/dev/api
# fullname = type + id (note that reddit doesn't follow this convention consistently)
# link = a post with a comment section
# comment = comment

header = {'user-agent': 'part two user agent'} # required for rate limiting
BASE_URL = "http://www.reddit.com"
LINK_EX = "r/pics/comments/324ln7/a_giant_boulder_fell_on_the_highway_in_ohio"
COMMENT_EX_1 = "cq7t7ka" # a top-level comment
COMMENT_EX_2 = "cq7vl6s" # a reply to a top-level comment


# OTHER HELPERS

# creates a url
def make_url(*args):
    ret = BASE_URL
    for add in args: ret = ret + "/" + add
    return ret + ".json"

# takes in a fullname of a thing "tn_abc..." and returns n == 3
def is_link_name(fullname): return fullname[1:2] == '3'

# takes in a fullname of a thing "tn_abc..." and returns its id "abc..."
def rm_type(fullname): return fullname[3:]

# returns the replies to the given link or comment
def get_replies(data, is_link):
    ret = data[1]['data']['children']
    if not is_link: ret = ret[0]['data']['replies']['data']['children']
    return ret

# returns the main data for a given JSON return object
# section = 0 for link, 1 for comment
def get_meta_data(data, section): return data[section]['data']['children'][0]['data']


# IMPL HELPERS

# iterates through all children of parent to find the number of ...
# ... direct replies before created_utc
# does the comment_tree looper
def gnpr_helper(comment_tree, created_utc):
    for comment in comment_tree:
        data = comment['data']
        if comment['kind'] == 'more':
            print('more', data['count'])
        else:
            print(data['score'])

# main
def get_num_prior_replies(parent_fullname, created_utc):
    parent_id = rm_type(parent_fullname)
    is_link = is_link_name(parent_fullname)
    if is_link:
        parent_url = make_url(parent_id)
    else:
        parent_url = make_url(LINK_EX, parent_id)
    data = requests.get(parent_url, headers=header).json()
    return gnpr_helper(get_replies(data, is_link), created_utc)

# MAIN
def get_data(url, is_comment_url):
    data = requests.get(url, headers=header).json()
    meta_data = get_meta_data(data, 1 if is_comment_url else 0)

    # starting from top

    # starting from bottom
    if is_comment_url:
        print('analyzing comment: ' + url)

         # grr, reddit doesn't follow its own naming conventions from the API
        parent_fullname = meta_data['parent_id']

        # the number of replies that have same direct parent ...
        # ... and were posted before this
        num_prior_replies = get_num_prior_replies(
            parent_fullname, meta_data['created_utc'])
        print(num_prior_replies)
    else:
        print('analyzing link: ' + url)

get_data(make_url(LINK_EX, COMMENT_EX_1), True)
time.sleep(2)
get_data(make_url(LINK_EX, COMMENT_EX_2), True)
