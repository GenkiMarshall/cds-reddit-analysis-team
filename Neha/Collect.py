#!/usr/bin/env python

import praw
import unicodedata
user_agent = ("Neha Desh user-agent")
r = praw.Reddit(user_agent=user_agent)
submission = r.get_submission(submission_id='2p3lzc')
flat_comments = praw.helpers.flatten_tree(submission.comments)

commento=[]
for comment in flat_comments:
      if isinstance(comment,praw.objects.MoreComments)==False:
           cms=unicodedata.normalize('NFKD',comment.body).encode('ascii','ignore')
           commento.append(cms)

file = open("/Users/nvd6/cds-reddit-analysis-team-2015/Neha/foo.txt","wb")
for body in commento:
       file.write(body)
