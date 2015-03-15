'''
Created on Mar 13, 2015

@author: Alice
'''
from TBase import TBase
import json
import Util
class T3(TBase):
    '''
    this is a link that extends TBase
    '''


    def __init__(self, json_obj):
        '''
        initialize a link from a json object (from reddit.com or file)
        :param json_obj: the json object to init from
        :type json_obj: dictionary
        '''
        #I'm going to have to set some variables to initialize a base 
        #comment with this link
        json_obj["link_id"] = json_obj["name"]
        #this has no parent, so well call it's parent the subreddit
        json_obj["parent_id"] = json_obj["subreddit_id"]
        #we know it's its own author
        json_obj["link_author"] = json_obj["author"]
        json_obj["body"] = json_obj["title"] + " " + json_obj["url"] + " " + json_obj["selftext"]
        
        super(T3, self).__init__(json_obj)
        
        
        self.upvote_ratio = json_obj["upvote_ratio"]
        self.url = json_obj["url"]
        self.title = json_obj["title"]
        self.selftext = json_obj["selftext"]
    

    
  
     
        
        