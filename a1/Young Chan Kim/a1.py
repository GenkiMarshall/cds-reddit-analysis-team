# April 29, 2015
# Young Chan Kim

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


def isMod(a):
	"""Return True if this author is a moderator in any subreddit.
	Precondition: a is a string of the author's name.
	"""
	url = 'http://www.reddit.com/user/' + a + '/about.json'
	d = getJSONData(url)
	return d['data']['is_mod']


def isVerified(a):
	"""Return True if this author is linked to a verified email address.
	Precondition: a is a string of the author's name.
	"""
	url = 'http://www.reddit.com/user/' + a + '/about.json'
	d = getJSONData(url)
	return d['data']['has_verified_email']


def isGold(a):
	"""Return True if this author is gold.
	Precondition: a is a string of the author's name.
	"""
	url = 'http://www.reddit.com/user/' + a + '/about.json'
	d = getJSONData(url)
	return d['data']['is_gold']


def getCreatedUTC(a):
	"""Return the date this author's account was created (Unix timestamp in seconds)
	Precondition: a is a string of the author's name.
	"""
	url = 'http://www.reddit.com/user/' + a + '/about.json'
	d = getJSONData(url)
	return d['data']['created_utc']


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

		# store author's threads' json data
		theurl = 'http://www.reddit.com/user/' + a + '/submitted.json?sort=new&count=25&after=' + d['data']['after']
		d = getJSONData(theurl)

	thelist.extend(d['data']['children'])
	thelist = sorted(thelist, key= lambda k : k['data']['created_utc'])

	return thelist


def haveAllComments(a):
	"""Return True if there are less than 950 comments collected for this author.
	Precondition: a is a string of the author's name.
	"""
	commentsList = getListOfCommentsChildren(a)
	return getNumComments(commentsList) < 950


def haveAllThreads(a):
	"""Return True if there are less than 950 threads collected for this author.
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
	"""Return the Unix time of the first observed post of this author, -1 if there are
	no posts for this author.
	Precondition: a is a string of the author's name.
	"""
	commentsList = getListOfCommentsChildren(a)
	threadsList = getListOfThreadsChildren(a)
	if (commentsList == [] and threadsList == []):
		return -1
	elif (commentsList == []):
		return threadsList[-1]['data']['created_utc']
	elif (threadsList == []):
		return commentsList[-1]['data']['created_utc']
	else:
		return max(commentsList[-1]['data']['created_utc'], threadsList[-1]['data']['created_utc'])


def getLastObservedPost(a):
	"""Return the Unix time of the last observed post of this author. -1 if there are
	no posts for this author.
	Precondition: a is a string of the author's name.
	"""
	commentsList = getListOfCommentsChildren(a)
	threadsList = getListOfThreadsChildren(a)
	if (commentsList == [] and threadsList == []):
		return -1
	elif (commentsList == []):
		return threadsList[0]['data']['created_utc']
	elif (threadsList == []):
		return commentsList[0]['data']['created_utc']
	else:
		return min(commentsList[0]['data']['created_utc'], threadsList[0]['data']['created_utc'])






#Tester

snopedlist = ['UsefulCongressman', 'Rednblu777', 'defendsTheUnpopular', 'kmcm07', 'franki-fig', 'BreezyBay', 
'vweight', 'beatlesfanatic64', 'Political_Lemming', 'Harvey66', '--moose--', 'ArchStantonsDead', 
'ThunderwearUnderwear', 'deckerparkes', 'ai0001', 'dielon108', 'gpsfan', '1776ftw', 'some_a_hole', 
'NeonClawsOfGamblor', 'ThrowAway65428', 'deep_fried_pork', 'portugalthephilosoph', 'izzbizz', 
'Canttakethewhyfromme', 'rudecanuck', 'Strood', 'Jug_Heads_Revenge', 'Anewfamily', 'Snyderrr', 'lagirl80', 
'DapperJD', 'Mr_Munchy', 'crackie_chan', 'wtfiswrongwithit', 'VioletHood', 'epsilonleqzero', 
'FascistRickScott', 'iwasnotshadowbanned', 'I_am_the_cloud']

# print the fields in JSON format
jsonResult = []
for snoped in snopedlist:
	child = {}

	url = 'http://www.reddit.com/user/' + snoped + '/about.json'
	d = getJSONData(url)

	child['is_mod'] = d['data']['is_mod']
	child['is_verified'] = d['data']['has_verified_email']
	child['is_gold'] = d['data']['is_gold']
	child['created_utc'] = d['data']['created_utc']
	child['total_link_karma'] = d['data']['link_karma']
	child['total_comment_karma'] = d['data']['comment_karma']
	
	child['total_comment_number'] = getNumComments(getListOfCommentsChildren(snoped))
	child['total_link_number'] = getNumThreads(getListOfThreadsChildren(snoped))

	child['first_observed_post'] = getFirstObservedPost(snoped)
	child['last_observed_post'] = getLastObservedPost(snoped)

	jsonResult.append(child)

print json.dumps(jsonResult)







