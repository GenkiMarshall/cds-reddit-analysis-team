with open('authors2.txt') as f:
    sumLinkKarma = 0.0;
    numberofAuthors = 0;
    for line in f:
        words = line.split();
        name = words[0];
        linkKarma = words[2];
        try:
            int('')
        except ValueError:
            sumLinkKarma = sumLinkKarma + int(linkKarma) 
        userID = words[4];
        numberofAuthors += 1;
        print('name: ' + words[0] + ' linkKarma: ' + words[2] + ' id: ' + words[4]);
    
    print (sumLinkKarma);
        
