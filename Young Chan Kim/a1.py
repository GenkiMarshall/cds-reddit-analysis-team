#April 10, 2015

import requests
import json
import time

#input author's name
author = raw_input('Type a Reddit author\'s name')

# reddit requires user-agent for rate limiting
header = {'user-agent': 'Young user agent'}
# store author's json data
url = 'http://www.reddit.com/user/' + author + '/about.json'
response = requests.get(url, headers=header)
data = response.json()

if (data['kind'] == 't2'):
	is_mod = data['data']['is_mod']
	is_verified = data['data']['has_verified_email']
	is_gold = data['data']['is_gold']
	created_utc = data['data']['created_utc']

	time.sleep(2) #cannot request more than once every 2 seconds
	# store author's comments/threads' json data
	url2 = 'http://www.reddit.com/user/' + author + '/comments.json?sort=new'
	response2 = requests.get(url2, headers=header)
	data2 = response2.json()

	fullList = getFullListOfChildren(data2, author, header)

	tupl = getNumCommentsAndThreads(fullList)
	have_all_comments = tupl[0] < 950
	have_all_threads = tupl[1] < 950

	first_observed_post = fullList[0]['data']['created_utc']
	last_observed_post = fullList[-1]['data']['created_utc']




def getFullListOfChildren(d, a, h):
	"""Return a list containing all children (dictionaries) for this user's comments/threads data.
	This list must be sorted according each child's 'created_utc' field.
	Precondition: d is a dictionary containing information about author's comments/threads. a is a
	string of the author's name. h is the header for user agent.
	"""
	thelist = []

	while (d['data']['after'] != 'null'):
		thelist.extend(d['data']['children'])

		time.sleep(2) #cannot request more than once every 2 seconds
		# store author's comments/threads' json data
		theurl = 'http://www.reddit.com/user/' + a + 
			'/comments.json?sort=new&count=25&after=' + d['data']['after']
		theresponse = requests.get(theurl, headers=h)
		d = theresponse.json()

	thelist.extend(d['data']['children'])
	thelist = sorted(thelist, key= lambda k : k['created_utc'])

	return thelist


def getNumCommentsAndThreads(children):
	"""Return a tuple containing (1): the number of comments this author has
	and (2): the number of threads this author has.
	Precondition: children is a list of dictionaries containing information about author's 
	comments/threads.	
	"""
	numComments = 0
	numThreads = 0

	for child in children:
		if (child['kind'] == 't1'):
			numComments += 1
		if (child['kind'] == 't3'):
			numThreads += 1

	return (numComments, numThreads)









