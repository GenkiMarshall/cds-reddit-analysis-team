'''
Created on Mar 14, 2015

@author: Alice
'''
from TBase import TBase
import json
def get_all_comments_from_file(file_name):
    '''
    load all the comments at once. let the world burn
    :param file_name: file name with json comments (1 per line)
    :type file_name: string
    :return list of TBase comments from your file 
    '''
    reader = file.open(file_name, "r")
    comments = []
    for line in reader:
        comments.append(TBase(json.JSONDecoder(line)))
    return comments 

class CommentFileStream(object):
    '''
    creates a stream from a json file, 
    this is used to avoid repulling 
    comments already seen (you must 
    save your comments to this file, with 1 per line)
    '''
    


    def __init__(self, file_name):
        '''
        
        :param file_name: file where json comments are stored
        :type file_name: string
        '''
        self.file = open(file_name, "r")
        self.oldest_id_seen = 0
        
        
    def get_next(self):
        '''
        returns one TBase comment at a time.
        Will block if it needs to pull more TBase comments
        '''
        line = self.file.readline()
        if line is None or line == "":
            return None
        print line
        try:
            comment = TBase(json.loads(line), True)
            if self.oldest_id_seen == 0 or comment.id < self.oldest_id_seen:
                self.oldest_id_seen = comment.id
            return comment
        except:
            return self.get_next()
        
            
    def close(self):
        self.file.close()