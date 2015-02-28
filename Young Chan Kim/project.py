#February 27, 2015

import urllib2
import json
import time

#store json data
request = urllib2.Request('http://www.reddit.com/r/nba/top/.json?sort=top&t=month')
response = urllib2.urlopen(request)
data = json.loads(response.read())
response.close()

#get the dictionary containing the main links
children = data[1]['data']['children']

#initialize dictionary to store comments
comments_dict = {}
#loop through the children to get each link
for c in children:
	if c['kind'] == 't3':
		permalink = c['data']['permalink']
		link = 'http://www.reddit.com' + permalink + '.json?sort=top&t=month'
		title = c['data']['title']

		time.sleep(2) #cannot request more than once every 2 seconds

		#store json data
		request2 = urllib2.Request(link)
		response2 = urllib2.urlopen(request2)
		link_data = json.loads(response2.read())
		response2.close()

		#initialize list to store this link's comments (and their replies?)
		this_link_comments = []

		#get the dictionary containing the main comments
		link_children = link_data[1]['data']['children']
		#loop through the children to get each comment
		for lc in link_children:
			if lc['kind'] == 't1':
				comment = lc['data']['body']
				this_link_comments.append(comment)

				#get the dictionary containing all the replies to this comment
				replies = lc['data']['replies']
				#get each reply
				




		#assign this list of comments as a value to the key (title of the link)
		comments_dict[title] = this_link_comments



for t in comments_dict:
	#parse t (which is the title)
	for comment in comments_dict[t]:
		#parse comment






