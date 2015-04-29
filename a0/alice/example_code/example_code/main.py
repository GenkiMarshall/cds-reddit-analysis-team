'''
Created on Mar 14, 2015

@author: Alice
'''
from CommentStream import CommentStream 
from UrlHandler import UrlHandler
from CommentFileStream import CommentFileStream
import sys
import json
import LinkIDStream
import matplotlib.pyplot as plt
from example_code.LinkIDStream import LinkIdStream

def something(comments_seen, comments_created, comment, date_to, date_from):
    '''
    An helper for an example for paging through reddit anylistics. Currently not working
    as reddit analytiscs history is not present
    
    this is set up to count the number of replies to comments with at least one reply
    inside a certain date by putting them in the appropriate set 
    
    :param comments_seen: ids of comments seen replied to so far will be kept here
    :type comments_seen: dictionary
    :param comments_created: ids of comments that were in seen but have now also been created (no comment can be
    replied to before it is created, so we start keeping track of them by day, total replies, total comments that got a reply
    at all
    :type comments_created: list
    :param comment: TBase comment to look at
    :type comment: TBase
    :param date_to: last date were willing to consider comments from
    :type date_to: Long
    :param date_from: comments have to be older than this to be considered
    :type date_from: long
    '''
    if comment.created_utc < date_to and comment.created_utc > date_from:
        if comment.parent_id in comments_seen:
            comments_seen[comment.parent_id]["replies"] = comments_seen[comment.parent_id]["replies"] + 1
        else:
            comments_seen[comment.parent_id] = {"replies" : 1}
        if comment.id in comments_seen:
            day = (comment.comment_created - date_from) % (24 *60 *60)
            if day in comments_created:
                comments_created[day]["replies"] = comments_created[day]["replies"] + comments_seen[comment.id]["replies"]
                comments_created[day]["comments"] = comments_created[day]["comments"] + 1
            else:
                comments_created[day] = {"replies" : comments_seen[comment.id]["replies"], "comments" : 1}
def example_of_reply_counting_in_r_conspiricy():
    '''
    Currently not working as reddit analytiscs history is not present
    
    this is set up to count the number of replies to comments with at least one reply
    inside a certain date by putting them in the appropriate set 
    '''
    previous_file = True
    oldest_id_seen = 0
    date_from = 1425081600
    date_to = 1426408563
    comments_seen = {}
    comments_created = []
    if previous_file:
        old_comment_file = CommentFileStream("old_comments.json")
        next_comment_from_file = old_comment_file.get_next()
        while (next_comment_from_file is not None):
            #do something with comment here
            something(comments_seen, comments_created, next_comment_from_file, date_to, date_from)
            next_comment_from_file = old_comment_file.get_next()
        old_comment_file.close()
        oldest_id_seen = old_comment_file.oldest_id_seen
    url_handler = UrlHandler("alice is awesome")
    comment_stream = CommentStream("subreddit=conspiracy", url_handler, oldest_id_seen)
    stop_url = False
    tries = 0 
    save_comments_file = open("old_comments.json", "a+")
    last_date = 0
    while not stop_url:
        
        try: 
            comment = comment_stream.get_next_comment()
            if comment is not None:
                save_comments_file.write(json.dumps(vars(comment)) + "\n")
                something(comments_seen, comments_created, comment, date_to, date_from)
                last_date = comment.created_utc
            #do something with comment
            tries = 0
        except IOError:
            e = sys.exc_info()
            print e 
            tries = tries + 1
            
        finally:
            stop_url = tries > 20 or (last_date > 0 and last_date < date_from) or comment_stream.done
    i = 0;
    comp = []
    while i < len(comments_created):
        comp[i] = comments_created[i]["replies"]/float(comments_created[i]["comments"])
    print comp
    plt.hist(comp, 200)
    plt.show()

def get_a_link_with_all_comments():
    '''
    Get a link and all attached comments (will be accessable through T.children() )
    This example has to look at more children a lot (more calls to server)
    :return T3
    '''
    url_handler = UrlHandler("alice is awesome")
    return url_handler.grab_link_data("2z18a7", False, True)
def get_a_link_but_dont_bother_with_comments():
    '''
    just create a T3 but don't bother attaching the children
    :return T3
    '''
    url_handler = UrlHandler("alice is awesome")
    return url_handler.grab_link_data("2z18a7", False, False)
def link_ids():
    '''
    Just get a bunch of link ids
    '''
    url_handler = UrlHandler("alice is awesome")
    link_id_stream = LinkIDStream.LinkIdStream(url_handler)
    link_file = open("link_ids.txt", "a+")
    while True:
        link_file.write(link_id_stream.get_next_link_id() + "\n");
    