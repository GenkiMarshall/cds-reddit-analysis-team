#March 13, 2015

import requests
import json
import time
import matplotlib.pyplot as plt

# Purpose: Plot the frequency of the occurrence of a certain word or name by time of 
# day in the past month

#the string to look for in each title, comment. and reply
keyword = raw_input('Type an NBA player\'s first or last name, a team name, or a word: ')
#the title of the plot that will be displayed
plot_title = 'Frequency of ' + keyword + ' by Hour of Day in the Past Month\'s NBA Subreddit'

def dfs_Comments_Replies(repliesdict, countlist, word):
	"""Recursive procedure that traverses through all of the replies found in repliesdict 
	and maps the hours of day (the corresponding indices) in countlist to the frequency of 
	the occurrence of word in each reply.
	Precondition: repliesdict is either '' or a dictionary containing replies. 
	countlist is a list containing the hours of day as indices mapped to int values.
	word is a string.
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

			countlist[hour_of_day] += count_Frequency(reply, word)
			
			dfs_Comments_Replies(x['data']['replies'], countlist, word)

def count_Frequency(s1, s2):
	"""Return the frequency of s2 occurring in s1.
	Precondition: s1 and s2 are both strings.
	"""
	count = 0
	for word in s1.split(' '):
		if s2.lower() in word.lower():
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

#initialize list to map hour of day to the frequencies of the word in all titles, 
#comments, and replies of the subreddit.
comments_list = []
for x in range(24):
	comments_list.append(0)

#loop through the children to access each link
for c in children:
	if c['kind'] == 't3':
		title = c['data']['title']

		#get the time of post and store the hour of day
		loc_time = time.localtime(c['data']['created_utc'])
		hour_of_day = loc_time.tm_hour

		comments_list[hour_of_day] += count_Frequency(title, keyword)

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

				comments_list[hour_of_day] += count_Frequency(comment, keyword)

				#get the dictionary containing all the replies to this comment
				replies = lc['data']['replies']
				#access each reply recursively/iteratively
				dfs_Comments_Replies(replies, comments_list, keyword)



if (comments_list != []):
	plt.plot(comments_list)
	plt.title(plot_title)
	plt.xlabel('Hour of Day')
	plt.ylabel('Frequency')
	plt.show()


