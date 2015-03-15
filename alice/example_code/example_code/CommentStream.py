'''
Created on Mar 14, 2015

@author: Alice
'''

class CommentStream(object):
    '''
    A comment stream to be used with reddit analyitics
    '''


    def __init__(self, get_args, url_handler, after = 0):
        '''
        
        :param get_args: the get arguments
        :type get_args: string (ex: 'subreddit="aww"&count=25' )
        :param url_handler: UrlHandler you are using, you should only create 1 per program run
        :type url_handler: UrlHandler
        :param after: base 10 comment ID to look before
        :type after: long
        '''
        self.url_handler = url_handler
        self.comments = []
        self.next_call = lambda : self.url_handler.page_reddit_analytics(get_args, after)
        self.done = False #indicates comment stream has been exhausted
        
    def get_next_comment(self):
        '''
        gets the next comment, blocks if it needs to retrieve more
        :return TBase comment or None if no more comments can be retrieved
        '''
        if len(self.comments) == 0 and not self.done:

            try: 
                hold = self.next_call()
                self.done = hold is None
                self.comments = hold["comments"]
                self.next_call = hold["next_call"]
            except:
                print "could not get next comment"
                
        if not self.done:
            return self.comments.pop(0)
        return None