#! /usr/bin/python

import json
import urllib2
import csv
import requests

header = {'user-agent': 'genki marshall user agent'}
url = 'http://www.reddit.com/r/AMA/.json'
r = requests.get(url, headers=header)
childrenList=r.json()['data']['children']

csvfile = open('RedditAMAData.csv', 'wb')
redditWriter=csv.writer(csvfile, delimiter=',')
for item in childrenList:
       data=item['data']
       csvList=[];
       csvList.append(data['id'])
       csvList.append(data['title'])
       csvList.append(data['selftext'])
       csvList.append(data['url'])
       csvList.append(data['author'])
       csvList.append(data['likes'])
       csvList.append(data['score'])
       csvList.append(data['num_comments'])
       print csvList  
       redditWriter.writerow(csvList)
    
    


