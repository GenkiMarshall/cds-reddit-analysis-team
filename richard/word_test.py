import time
import requests
text = raw_input('What text would you like to search for? ')
num = int(raw_input('Top how many posts from each subreddit this month? '))
url0 = 'http://www.reddit.com/subreddits/popular/.json'
header = {'user-agent': 'yay personal text'}
subs = requests.get(url0, headers=header)
for i in subs.json()['data']['children']:
  time.sleep(2)
  sub = i['data']['display_name']
  url = 'http://www.reddit.com/r/' + sub + '/top.json?t=month&limit=' + str(num)
  header = {'user-agent': 'yay personal text'}
  r = requests.get(url, headers=header)
  sum = 0
  for j in r.json()['data']['children']:
    if text in j['data']['title']:
      sum += 1
  print sub + ': ' + str(sum) + ' posts have "' + text + '" in the title'