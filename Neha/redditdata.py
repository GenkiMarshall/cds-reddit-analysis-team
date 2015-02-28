#! /usr/bin/python

import json
import urllib2
import csv

f=urllib2.urlopen('http://www.reddit.com/r/AMA/.json')
jsonDict=json.loads(f.read())
childrenList=jsonDict['data']['children']
for item in childrenList:
    data=item['data']
    Id=data['id']
    title=data['title']
    selftext=data['selftext']
    urlink=data['url']
    author=data['author']
    likes=data['likes']
    score=data['score']
    numComments=data['num_comments']
    ups=data['ups']
    with open('RedditAMAData.csv', 'wb') as csvfile:
           redditWriter=csv.writer(csvfile, delimiter=',')
           redditWriter.writerow([Id,title,selftext,urlink,author,likes,score,numComments,ups])
    
    


