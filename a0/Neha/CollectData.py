#!/usr/bin/env python

import praw
import unicodedata
user_agent = ("genki marshall user agent")
r = praw.Reddit(user_agent=user_agent)
submission = r.get_submission(submission_id='2p3lzc')
submission.replace_more_comments(limit=None, threshold=0)
flat_comments = praw.helpers.flatten_tree(submission.comments)

commento=[]
for comment in flat_comments:
      if isinstance(comment,praw.objects.MoreComments)==False:
           cms=unicodedata.normalize('NFKD',comment.body).encode('ascii','ignore')
           commento.append(cms)
file = open("foo.txt","wb")
for body in commento:
       file.write(body)
