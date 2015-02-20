#! /bin/python2

import httplib

# specify user header
# http://stackoverflow.com/questions/13213048/urllib2-http-error-429
hdr= { 'User-Agent' : 'genki marshall super user agent' }
conn = httplib.HTTPConnection('www.reddit.com')
conn.request('GET', '/r/unixporn/top.json?t=month&limit=2', headers=hdr)
print conn.getresponse().read()
conn.close()
