'''
Created on Mar 13, 2015

@author: Alice
'''
import json
import Util
import T
import string
class TBase(T.T):
    '''
    classdocs
    '''
    def __url_title_maker(self, title):
        '''
        used to make the title for urls. This is part of the url needed for comments
        :param title: title of the link
        :type title: string
        :return title formated for url
        '''
        title = title.lower() 
        title = title.replace_all(' ', '_')
        keep = string.ascii_lowercase + '_1234567890'
        title = ''.join(ch for ch in title if ch in keep)
        if len(title) < 51:
            return title
        else:
            title = title[0:51]
            title = title[0:title.rindex('_')]
            return title

    def __init__(self, json_reddit_analytics_obj, from_file = False):
        '''
        This initiallizes a comment from file (using it's own print), from reddit.com, or from redditanylitics
        :param json_reddit_analytics_obj: a disctionary from any of ^ places
        :type json_reddit_analytics_obj: Dictionary
        :param from_file: is this being loaded from file?
        :type from_file: boolean
        '''
        if not from_file:
            super(TBase, self).__init__(Util.base36decode(json_reddit_analytics_obj["id"]), json_reddit_analytics_obj["name"][:2], json_reddit_analytics_obj["created_utc"])  
            self.created_utc = json_reddit_analytics_obj["created_utc"]
            self.author_flair_text = json_reddit_analytics_obj["author_flair_text"]
            self.subreddit_id = Util.base36decode(json_reddit_analytics_obj["subreddit_id"][3:])
            self.link_id = Util.base36decode(json_reddit_analytics_obj["link_id"][3:])
            self.parent_id = Util.base36decode(json_reddit_analytics_obj["parent_id"][3:])
            self.parent_kind = json_reddit_analytics_obj["parent_id"][:2]
            self.kind = json_reddit_analytics_obj["name"][:2]
            self.author = json_reddit_analytics_obj["author"]
            self.score = json_reddit_analytics_obj["score"]
            self.subreddit = json_reddit_analytics_obj["subreddit"]
            self.link_author = json_reddit_analytics_obj["link_author"]
            self.name = json_reddit_analytics_obj["name"]
            self.body = json_reddit_analytics_obj["body"]
            self.author_flair_css_class = json_reddit_analytics_obj["author_flair_css_class"]
            self.parent_author_id = "";
            self.__json_url = None
            if "permalink" in json_reddit_analytics_obj:
                self.__json_url = "http://www.reddit.com" + json_reddit_analytics_obj["permalink"] + ".json"
            elif "link_url" in json_reddit_analytics_obj:
                self.__json_url = json_reddit_analytics_obj["link_url"] + Util.base36encode(self.id) + ".json"
            elif "link_title" in json_reddit_analytics_obj:
                self.__json_url = 'http://www.reddit.com/comments/' 
                + Util.base36encode(self.link_id) + "/" 
                + self.__url_title_maker(json_reddit_analytics_obj["link_title"]) 
                + "/" + Util.base36encode(self.id) + ".json"
        else:
            super(TBase, self).__init__(json_reddit_analytics_obj["id"], json_reddit_analytics_obj["name"][:2], json_reddit_analytics_obj["created_utc"])  
            self.created_utc = json_reddit_analytics_obj["created_utc"]
            self.author_flair_text = json_reddit_analytics_obj["author_flair_text"]
            self.subreddit_id = json_reddit_analytics_obj["subreddit_id"]
            self.link_id = json_reddit_analytics_obj["link_id"]
            self.parent_id = json_reddit_analytics_obj["parent_id"]
            self.parent_kind = json_reddit_analytics_obj["parent_kind"]
            self.kind = json_reddit_analytics_obj["kind"]
            self.author = json_reddit_analytics_obj["author"]
            self.score = json_reddit_analytics_obj["score"]
            self.subreddit = json_reddit_analytics_obj["subreddit"]
            self.link_author = json_reddit_analytics_obj["link_author"]
            self.name = json_reddit_analytics_obj["name"]
            self.body = json_reddit_analytics_obj["body"]
            self.author_flair_css_class = json_reddit_analytics_obj["author_flair_css_class"]
            self.parent_author_id = "";
            self.__json_url = json_reddit_analytics_obj["_TBase__json_url"]
            
        
   
    
        
        

    def get_json_url(self):
        '''
        get the json url where this comment or link can be reached, make it if it's not
        made but the parent_link has been found (an obscure case)
        '''
        if not self.__json_url is None:
            return self.__json_url 
        else:
            parent_link = self.get_link()
            if parent_link is not None:
                self.__json_url = parent_link[:-4] + "/" + Util.base36encode(self.id)  + ".json"
        return self.__json_url

       
        