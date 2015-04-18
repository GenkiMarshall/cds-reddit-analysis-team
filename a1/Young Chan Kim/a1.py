#April 17, 2015

import requests
import json
import time


def getJSONData(url):
	"""Return the dictionary containing the JSON data corresponding to this url.
	Precondition: url is a string of a valid url.
	"""
	# reddit requires user-agent for rate limiting
	header = {'user-agent': 'Young user agent'}
	response = requests.get(url, headers=header)
	data = response.json()
	return data


def getListOfCommentsChildren(a):
	"""Return a list containing all children (dictionaries) for this author's comments data.
	This list must be sorted according each child's 'created_utc' field.
	Precondition: a is a string of the author's name.
	"""
	# store author's comments' json data
	url = 'http://www.reddit.com/user/' + a + '/comments.json?sort=new'
	d = getJSONData(url)

	thelist = []

	while (not (d['data']['after'] is None)):
		thelist.extend(d['data']['children'])

		time.sleep(2) #cannot request more than once every 2 seconds
		# store author's comments' json data
		theurl = 'http://www.reddit.com/user/' + a + '/comments.json?sort=new&count=25&after=' + d['data']['after']
		d = getJSONData(theurl)

	thelist.extend(d['data']['children'])
	thelist = sorted(thelist, key= lambda k : k['data']['created_utc'])

	return thelist


def getListOfThreadsChildren(a):
	"""Return a list containing all children (dictionaries) for this author's threads data.
	This list must be sorted according each child's 'created_utc' field.
	Precondition: a is a string of the author's name.
	"""
	# store author's threads' json data
	url = 'http://www.reddit.com/user/' + a + '/submitted.json?sort=new'
	d = getJSONData(url)

	thelist = []

	while (not (d['data']['after'] is None)):
		thelist.extend(d['data']['children'])

		time.sleep(2) #cannot request more than once every 2 seconds
		# store author's threads' json data
		theurl = 'http://www.reddit.com/user/' + a + '/submitted.json?sort=new&count=25&after=' + d['data']['after']
		d = getJSONData(theurl)

	thelist.extend(d['data']['children'])
	thelist = sorted(thelist, key= lambda k : k['data']['created_utc'])

	return thelist


def haveAllComments(a):
	"""Return True if the are there less than 950 comments collected for this author.
	Precondition: a is a string of the author's name.
	"""
	commentsList = getListOfCommentsChildren(a)
	return getNumComments(commentsList) < 950


def haveAllThreads(a):
	"""Return True if the are there less than 950 threads collected for this author.
	Precondition: a is a string of the author's name.
	"""
	threadsList = getListOfThreadsChildren(a)
	return getNumThreads(threadsList) < 950


def getNumComments(children):
	"""Return the number of comments the author corresponding to this children has. This is a
	helper function for haveAllComments().
	Precondition: children is a list of dictionaries containing information about an author's 
	comments (all of them).	
	"""
	numComments = 0

	for child in children:
		if (child['kind'] == 't1'):
			numComments += 1

	return numComments


def getNumThreads(children):
	"""Return the number of threads the author corresponding to this children has. This is a
	helper function for haveAllThreads().
	Precondition: children is a list of dictionaries containing information about an author's 
	threads (all of them).	
	"""
	numThreads = 0

	for child in children:
		if (child['kind'] == 't3'):
			numThreads += 1

	return numThreads


def getFirstObservedPost(a):
	"""Return the Unix time of the first observed post of this author.
	Precondition: a is a string of the author's name.
	"""
	commentsList = getListOfCommentsChildren(a)
	threadsList = getListOfThreadsChildren(a)
	return min(commentsList[0]['data']['created_utc'], threadsList[0]['data']['created_utc'])


def getLastObservedPost(a):
	"""Return the Unix time of the last observed post of this author.
	Precondition: a is a string of the author's name.
	"""
	commentsList = getListOfCommentsChildren(a)
	threadsList = getListOfThreadsChildren(a)
	return max(commentsList[-1]['data']['created_utc'], threadsList[-1]['data']['created_utc'])


#Tester

#input author's name
author = raw_input('Type a Reddit author\'s name: ')

# store author's json data
url = 'http://www.reddit.com/user/' + author + '/about.json'
data = getJSONData(url)

if (data['kind'] == 't2'):
	is_mod = data['data']['is_mod']
	is_verified = data['data']['has_verified_email']
	is_gold = data['data']['is_gold']
	created_utc = data['data']['created_utc']

	time.sleep(2) #cannot request more than once every 2 seconds
	
	have_all_comments = haveAllComments(author)
	have_all_threads = haveAllThreads(author)

	first_observed_post = getFirstObservedPost(author)
	last_observed_post = getLastObservedPost(author)

	print 'is_mod: ' + str(is_mod) +'\n'
	print 'is_verified: ' + str(is_verified) + '\n'
	print 'is_gold: ' + str(is_gold) + '\n'
	print 'created_utc: ' + str(created_utc) + '\n'
	print 'have_all_comments: ' + str(have_all_comments) + '\n'
	print 'have_all_threads: ' + str(have_all_threads) + '\n'
	print 'first_observed_post: ' + str(first_observed_post) + '\n'
	print 'last_observed_post: ' + str(last_observed_post) + '\n'









