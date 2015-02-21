#February 20, 2015

import urllib2
import json
import datetime

#with urllib2.urlopen('http://www.reddit.com/r/aww/comments/2vrx59/husky_pup_stealing_from_a_ferret/.json') as f:
	#data = json.loads(f.read())

#print data


request = urllib2.Request('http://www.reddit.com/r/' +
	'aww/comments/2vrx59/husky_pup_stealing_from_a_' +
	'ferret/.json')
response = urllib2.urlopen(request)
data = json.loads(response.read())
response.close()


#get the main 31 comments and the times they were posted
children = data[1]['data']['children']

#comments = []
for c in children:
	if c['kind'] == 't1':
		comment = c['data']['body']
		time = c['data']['created_utc']
		realtime = datetime.datetime.utcfromtimestamp(time)

		print str(realtime) + '--> ' + comment
		
		#comments.append(c['data']['body'])
#print comments

