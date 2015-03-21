'''
Created on Mar 14, 2015

NOT CURRENTLY IN USE
@author: Alice
'''
from T import T
def get_about_url(author_name):
    return "http://www.reddit.com/user/" + author_name + "/about.json"

class T2():
    '''
    classdocs
    '''


    def __init__(self, author_json_obj, sup):
        self.name = "Z0MBGiEF",
        super(author_json_obj["name"], "t2", author_json_obj["created_utc"])
        
        
        self.link_karma = author_json_obj["link_karma"]
        self.comment_karma = author_json_obj["comment_karma"]
        self.is_gold =  author_json_obj["is_gold"]
        self.is_mod =  author_json_obj["is_mod"]
        self.has_verified_email =  author_json_obj["has_verified_email"]
        self.id =  author_json_obj["id"]
        