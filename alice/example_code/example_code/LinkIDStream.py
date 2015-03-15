'''
Created on Mar 14, 2015

@author: Alice
'''

class LinkIdStream(object):
    '''
    A stream for getting link ids from reddit.com/all/new
    '''


    def __init__(self, url_handler, after = None):
        '''
        
        :param url_handler: 
        :type url_handler:
        :param after: name to call after, with type and base 36 id (ex: "t3_dfjogj")
        :type after: string
        '''
        self.url_handler = url_handler
        self.link_ids = []
        self.next_call = lambda : self.url_handler.reddit_com_link_id_getter(after)

    
    def get_next_link_id(self):
        '''
        gets the next link id
        '''
        if len(self.link_ids)==0:

            try: 
                hold = self.next_call()
                self.link_ids = hold["link_ids"]
                self.next_call = hold["next_call"]
            except IOError:
                print "could not get next link set"
                
        
        return self.link_ids.pop(0)

    