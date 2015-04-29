with open('authors2.txt') as f:
    sumLinkKarma = 0.0;
    numberofAuthors = 0;
    for line in f:
        words = line.split();
        name = words[0];
        linkKarma = words[2];
        userID = words[4];
        numberofAuthors += 1;
        print('name: ' + words[0] + ' linkKarma: ' + words[2] + ' id: ' + words[4]);
        sumLinkKarma = sumLinkKarma + linkKarma;
    
    avg_linkKarma = sumLinkKarma / numberofAuthors;
    
    print(avg_linkKarma);