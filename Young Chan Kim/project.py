#March 06, 2015

#import urllib2
import requests
import json
import time

# Purpose: Plot the frequency of the occurrence the name Westbrook by time of day in the past month

#the string to look for in each title, comment. and reply
keyword = 'westbrook'

def dfs_Comments_Replies(repliesdict, countdict, name):
	"""Recursive procedure that traverses through all of the replies found in repliesdict 
	and maps the keys (hours of day) in countdict to the frequency of the occurrence of 
	name in each reply.
	Precondition: repliesdict is either '' or a dictionary containing replies. 
	countdict is a dictionary containing the hours of day as keys mapped to int values.
	name is a string.
	"""
	#base case (maximum depth reached when 'replies' has value '')
	if repliesdict == '':
		return
	#recursive case
	replies_children = repliesdict['data']['children']
	for x in replies_children:
		if (x['kind'] == 't1'):
			reply = x['data']['body']

			#get the time of reply and store the hour of day
			loc_time = time.localtime(x['data']['created_utc'])
			hour_of_day = loc_time.tm_hour

			countdict[str(hour_of_day)] += count_Frequency(reply, name)
			
			dfs_Comments_Replies(x['data']['replies'], countdict, name)

def count_Frequency(s1, s2):
	"""Return the frequency of s2 occurring in s1.
	Precondition: s1 and s2 are both strings.
	"""
	count = 0
	for word in s1.split(' '):
		if s2 in word.lower():
			count += 1
	return count

# reddit requires user-agent for rate limiting
header = {'user-agent': 'Young user agent'}
#store json data
url = 'http://www.reddit.com/r/nba/top/.json?count=100&sort=top&t=month'
response = requests.get(url, headers=header)
data  = response.json()

#get the dictionary containing the main links
children = data['data']['children']

#initialize dictionary to map hour of day to the frequencies of the name in all titles, 
#comments, and replies of the subreddit. Of the form {0: 0, 1: 0, ... , 23: 0}.
comments_dict = {}
for x in range(24):
	comments_dict[str(x)] = 0

#loop through the children to access each link
for c in children:
	if c['kind'] == 't3':
		title = c['data']['title']

		#get the time of post and store the hour of day
		loc_time = time.localtime(c['data']['created_utc'])
		hour_of_day = loc_time.tm_hour

		comments_dict[str(hour_of_day)] += count_Frequency(title, keyword)

		permalink = c['data']['permalink']
		link = 'http://www.reddit.com' + permalink + '.json?count=100&sort=top&t=month'

		time.sleep(2) #cannot request more than once every 2 seconds

		#store json data
		response2 = requests.get(link, headers=header)
		link_data = response2.json()

		#get the dictionary containing the main comments
		link_children = link_data[1]['data']['children']
		#loop through the children to access each comment
		for lc in link_children:
			if lc['kind'] == 't1':
				comment = lc['data']['body']

				#get the time of comment and store the hour of day
				loc_time = time.localtime(lc['data']['created_utc'])
				hour_of_day = loc_time.tm_hour

				comments_dict[str(hour_of_day)] += count_Frequency(comment, keyword)

				#get the dictionary containing all the replies to this comment
				replies = lc['data']['replies']
				#access each reply recursively/iteratively
				dfs_Comments_Replies(replies, comments_dict, keyword)


if (comments_dict != {}):
	for t in comments_dict:
		print t + ': ' + str(comments_dict[t])
		


