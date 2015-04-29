# April 24, 2015
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


def getWeeksOfLinks(t3List, totalWeeks, first):
    allWeeks = [None] * totalWeeks
    for n in range(totalWeeks):
        start_utc = first - n * 604800
        end_utc = start_utc - 604800
        allWeeks[n] = []
        for link in t3List:
            if (link['data']['created_utc'] > end_utc) and (link['data']['created_utc'] <= start_utc):
                allWeeks[n].append(link)
    return allWeeks

                
def getWeeksOfComments(t1List, totalWeeks, first):
    allWeeks = [None] * totalWeeks
    for n in range(totalWeeks):
        start_utc = first - n * 604800
        end_utc = start_utc - 604800
        allWeeks[n] = []
        for comment in t1List:
            if (comment['data']['created_utc'] > end_utc) and (comment['data']['created_utc'] <= start_utc):
                allWeeks[n].append(comment)
    return allWeeks




#Tester

#input author's name
author = raw_input('Type a Reddit author\'s name: ')

# get the fields
is_mod = isMod(author)
is_verified = isVerified(author)
is_gold = isGold(author)
created_utc = getCreatedUTC(author)
	
have_all_comments = haveAllComments(author)
have_all_threads = haveAllThreads(author)

first_observed_post = getFirstObservedPost(author)
last_observed_post = getLastObservedPost(author)

t3List = getListOfThreadsChildren(author)
t1List = getListOfCommentsChildren(author)

totalWeeks = int((first_observed_post - last_observed_post)/604800)
weeksOfLinks = getWeeksOfLinks(t3List, totalWeeks, first_observed_post)
weeksOfComments = getWeeksOfComments(t1List, totalWeeks, first_observed_post)

#print str(weeksOfLinks[1])
#print str(weeksOfComments[0][0]['data']['score'])

links_per_week = [None] * totalWeeks
links_karma_per_week = [None] * totalWeeks
comments_per_week = [None] * totalWeeks
comments_karma_per_week = [None] * totalWeeks

for n in range(totalWeeks):
    links_per_week[n] = len(weeksOfLinks[n])
    links_karma_per_week[n] = 0
    for a in range(len(weeksOfLinks[n])):
	links_karma_per_week[n] =  links_karma_per_week[n] + weeksOfLinks[n][a]['data']['score']
    comments_per_week[n] = len(weeksOfComments[n])
    comments_karma_per_week[n] = 0
    for b in range(len(weeksOfComments[n])):
	comments_karma_per_week[n] = comments_karma_per_week[n] + weeksOfComments[n][b]['data']['score']

print 'is_mod: ' + str(is_mod) +'\n'
print 'is_verified: ' + str(is_verified) + '\n'
print 'is_gold: ' + str(is_gold) + '\n'
print 'created_utc: ' + str(created_utc) + '\n'
print 'have_all_comments: ' + str(have_all_comments) + '\n'
print 'have_all_threads: ' + str(have_all_threads) + '\n'
print 'first_observed_post: ' + str(first_observed_post) + '\n'
print 'last_observed_post: ' + str(last_observed_post) + '\n'

print 'links_per_week: ' + str(links_per_week) + '\n'
print 'links_karma_per_week: ' + str(links_karma_per_week) + '\n'
print 'comments_per_week: ' + str(comments_per_week) + '\n'
print 'comments_karma_per_week: ' + str(comments_karma_per_week) + '\n'







