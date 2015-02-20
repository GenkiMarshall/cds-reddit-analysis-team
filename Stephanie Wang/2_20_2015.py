
# coding: utf-8

# In[1]:

import urllib2


# In[2]:

f = urllib2.urlopen('http://www.reddit.com/r/aww/comments/2vrx59/husky_pup_stealing_from_a_ferret/.json')


# In[3]:

data = f.read()


# In[4]:

data[:50]


# In[5]:

import json


# In[6]:

parsed_data = json.loads(data)


# In[7]:

print parsed_data


# In[ ]:



