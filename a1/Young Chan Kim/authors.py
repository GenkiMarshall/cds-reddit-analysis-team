#April 29, 2015
#Young Chan Kim

import a1
import requests
import json
import time

#Purpose: Obtain a list of author names to be used in a1.py

#input the name of the file containing all authors
filename = raw_input('Type the name of the file containing all authors: ')

# Process text file
file = open(filename)
thelist = []    
for line in file:
    if ('\n' in line):
        thelist.append(line[:-1])
    else:
        thelist.append(line)
file.close()

# Collect only the authors who were snoped
snopedlist = []
for x in thelist:
	authorInfo = x.split()
	if (int(authorInfo[1]) > 0):
		snopedlist.append(authorInfo)

# Clean out the errors (deleted accounts)
cleanlist = []
for info in snopedlist:
	url = 'http://www.reddit.com/user/' + info[0] + '/about.json'
	if (a1.getJSONData(url) != {'error': 404}):
		cleanlist.append(info)

# Limit to 40 most recent (greatest utc time) authors who were snoped
if (len(cleanlist) > 40):
	cleanlist = sorted(cleanlist, key= lambda k : a1.getCreatedUTC(k[0]))
	cleanlist = cleanlist[-40:]

authorlist = []
for c in cleanlist:
	authorlist.append(c[0])

print str(authorlist)








