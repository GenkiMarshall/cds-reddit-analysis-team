
# coding: utf-8

# In[1]:

import urllib2


# In[5]:

import json


# In[2]:

f = urllib2.urlopen('http://www.reddit.com/r/aww/comments/2vrx59/husky_pup_stealing_from_a_ferret/.json')


# In[3]:

data = f.read()


# In[6]:

parsed_data = json.loads(data)


# In[18]:

object = parsed_data[1]["data"]["children"]


# In[58]:

def getBody(object):
    body = []
    for child in object: #loop through 31 items in children
        if child["kind"] == "t1":
            body.append(child["data"]["body"])
    return body


# In[ ]:



