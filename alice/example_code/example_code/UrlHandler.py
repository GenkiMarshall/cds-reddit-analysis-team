'''
Created on Mar 14, 2015

@author: Alice
'''
import requests 
from datetime import datetime
from time  import sleep
import time
from TBase import TBase
import Util
from T3 import T3
from T import T
import T as TWrapper
from sqlalchemy.testing.plugin.plugin_base import after_test
class UrlHandler(object):
    '''
    This thing handles all the URL requests and timing between server calls
    '''
    
    
    def __init__(self, name):
        '''
        
        :param name: Name for the user agent
        :type name: String
        '''
        # reddit requires user-agent for rate limiting
        self.__last_reddit_analytics_call = long(0)
        self.__last_reddit_call = long(0)
        self.header = {'user-agent': name + ' user agent'}
        
        
    def page_reddit_analytics(self, args = "", after = 0):
        '''
        for paging through reddit anaylitics. Blocking
        :param args: the get_args (ex: subreddit=ama&count=25"
        :type args: String
        :param after: the last id seen, base 10
        :type after: long
        '''
        self.__check_time(self.__last_reddit_analytics_call) #check time of last call & wait
        url = "http://redditanalytics.com/api/getRecent.php?"
        if len(args) > 0:
            url = url + args
        if after > 0:
            url = url + "&after=" + str(after)
        print "accessing " + url
        
        all_data = requests.get(url, headers=self.header).json()
        
        self.__last_reddit_analytics_call = self.__nowzers_in_milli() #update time
        #end of reddit_anylitics data?
        stream_is_exhausted = all_data["metadata"]["newest_date"] == 0 and all_data["metadata"]["oldest_date"] == 9999999999
        if stream_is_exhausted:
            return None
        
        data = all_data["data"]
        comments = []
        for child in data:
            comments.append(TBase(child))
        metadata = all_data["metadata"]
        oldest_id = metadata["oldest_id"]
        next_call = lambda :  self.page_reddit_analytics(args, oldest_id)
        return {
                    'comments' : comments,
                    'metadata' : metadata,
                    'data'     : data,
                    'oldest_id' : oldest_id,
                    'next_call' : next_call #next call to make in this stream
                }
        
        
    def grab_link_data(self, link_id, is_base_10 = False, include_children = False):
        '''
        gets link data, and possibly all the comments to the link
        if specified, hooting them up through the parent
        child tree system in the base class T
        :param link_id: the id of the link
        :type link_id: string or long (long if in base 10)
        :param is_base_10: is the link in base 10 (it needs to be a long if so)
        :type is_base_10: boolean
        :param include_children: do you want to grab all the comments as well?
        :type include_children: boolean
        '''
        self.__check_time(self.__last_reddit_call)
        if (is_base_10):
            link_id = Util.base36encode(link_id)
        url = "http://www.reddit.com/comments/" + link_id + ".json"
        print "accessing " + url
        all_data = requests.get(url, headers=self.header).json()
        link = T3(all_data[0]["data"]["children"][0]["data"])
        self.__last_reddit_call = self.__nowzers_in_milli()
        if include_children:    
            hold = self.__grab_children_of_link(link, all_data[1])
            self.__match_up(link, link, hold)
        return link       
    
    def __grab_children_of_link(self, link, data):
        '''
        Helper method for grab_link_data
        :param link: T3 link we are harvesting the comments of
        :type link: T3
        :param data: the json object we are currently looking at (expected to have a "kind" field == t3 OR Listing OR more)
        :type data: dictionary
        :return None or TBase or TBase list representing direct replies to the calling object
        '''
        print data
        if "kind" in data:
            if data["kind"] == "t1":
                
                data["data"]["link_author"] = link.author
                comment = TBase(data["data"])
                if "replies" in data["data"]:
                    replies = self.__grab_children_of_link(link, data["data"]["replies"])
                    if replies is not None:
                        for reply in replies:
                        
                            self.__match_up(link, comment, reply)
                return comment
            if data["kind"] == "more":
                kids = []
                for idd in data["data"]["children"]:
                    url = link.get_json_url()[:-5]+""+idd+".json"
                    print link.get_json_url()
                    self.__check_time(self.__last_reddit_call)
                    print "accessing " + url
                    all_data = requests.get(url, headers=self.header).json()
                    self.__last_reddit_call = self.__nowzers_in_milli()
                    new_data = all_data[1]
                    new_reply = self.__grab_children_of_link(link, new_data)
                    if isinstance(new_reply, list):
                        kids.extend(new_reply)
                    elif isinstance(new_reply, TBase):
                        kids.append(new_reply)
                if len(kids) == 0:
                    return None
                elif len(kids) == 1:
                    return kids[0]
                else:
                    return kids
            if data["kind"] == "Listing":
                kids = [] 
                for child in data["data"]["children"]:
                    new_reply = self.__grab_children_of_link(link, child)
                    if new_reply is not None and isinstance(new_reply, TBase):
                        kids.append(new_reply)
                    elif new_reply is not None:
                        kids.extend(new_reply)
                return kids
                    
                     
                
                           
                           
    def __match_up(self, link, comment, reply_comment):
        '''
        helper method to build the trees for links 
        defind through parent and children fields of the class T
        :param link: link we are harvesting comments from
        :type link: T3
        :param comment: current direct parent comment (or link)
        :type comment: TBase
        :param reply_comment: reply_comment(s) currently being looked at
        :type reply_comment: None or TBase or TBase list
        '''
        if isinstance(reply_comment, list):
            for reply in reply_comment:
                self.__match_up(link, comment, reply)
        elif isinstance(reply_comment, TBase):
            print comment
            print reply_comment
            TWrapper.birth(comment, reply_comment)
            TWrapper.birth(link, reply_comment)

    def reddit_com_link_id_getter(self, after = None):
        '''
        This simply grabs a bunch of link ids
        :param after: name of last oldest link gotten (ex: t3_fgdkjd)
        :type after: string
        :return dictionary with link_ids and next_call
        '''
        self.__check_time(self.__last_reddit_call)
        base_url = "https://www.reddit.com/r/all/new/.json?"
        if after is not None:
            base_url = base_url + "after=" + after
        print "accessing " + base_url 
        kids = requests.get(base_url, headers=self.header).json()["data"]["children"]
        self.__last_reddit_call = self.__nowzers_in_milli()
        link_ids = []
        for kid in kids:
            link_ids.append(kid["data"]["name"])
            print kid
        print link_ids
        hold = link_ids[-1]
        new_call = lambda: self.reddit_com_link_id_getter(hold)
        return {"link_ids" : link_ids, "next_call" : new_call }    
            
    def __nowzers_in_milli(self):
        '''
        get the current time in milliseconds
        :return long
        '''
        now = datetime.now() 
        return time.mktime(now.timetuple())*1e3 + now.microsecond/1e3      
    def __check_time(self, time_to_check):
        '''
        blocks the program till it can call the current site again
        :param time_to_check: the last time the site being called was acessecd in milliseconds
        :type time_to_check: long
        '''
        current_time = self.__nowzers_in_milli()
        time_waited = current_time - time_to_check
        time_to_wait = 2000 - time_waited
        if (time_to_wait > 0):
            sleep(time_to_wait/1000.0)