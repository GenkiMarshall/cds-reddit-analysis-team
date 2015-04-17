#April 17 2015
#links
first_utc = first_observed_post[created_utc]
last_utc = last_observed_post[created_utc]
totalWeeks = (first_utc-last_utc)/604800
weeksOfLinks = getWeeksOfLinks(t3List,totalWeeks)
weeksOfComments = getWeeksOfComments(t1List,totalWeeks)

for n in range(totalWeeks):
    links_per_week[n] = len(weeksOfLinks[n])
    links_karma_per_week[n] = weeksOfLinks[n][score]
    comments_per_week[n] = len(weeksOfComments[n])
    comments_karma_per_week[n] = weeksOfComments[n][score]

def getWeeksOfLinks(t3List,totalWeeks):
    allWeeks = []
    for n in range(totalWeeks):
        start_utc = first_utc - n * 604800
        end_utc = start_utc - 604800
        allWeeks[n] = []
        for link in t3List:
            if (link[created_utc] > end_utc) and (link[created_utc] <= start_utc):
                allWeeks[n].append(link)
    return allWeeks
                
def getWeeksOfComments(t1List,totalWeeks):
    allWeeks = []
    for n in range(totalWeeks):
        start_utc = first_utc - n * 604800
        end_utc = start_utc - 604800
        allWeeks[n] = []
        for comment in t1List:
            if (comment[created_utc] > end_utc) and (comment[created_utc] <= start_utc):
                allWeeks[n].append(comment)
    return allWeeks