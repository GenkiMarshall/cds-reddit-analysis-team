#!/usr/bin/env python

from gensim import corpora, models,similarities
from itertools import chain
import nltk
from nltk.corpus import stopwords
from operator import itemgetter
import re
import praw
import unicodedata

user_agent = ("genki marshall user agent")
r = praw.Reddit(user_agent=user_agent)
submission = r.get_submission(submission_id='2p3lzc')
flat_comments = praw.helpers.flatten_tree(submission.comments)

documents=[]
for comment in flat_comments:
      if isinstance(comment,praw.objects.MoreComments)==False:
           cms=unicodedata.normalize('NFKD',comment.body).encode('ascii','ignore')
           documents.append(cms)
stoplist=stopwords.words('english')
texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
dictionary=corpora.Dictionary(texts)
corpus=[dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf=tfidf[corpus]
n_topics = 10
lda = models.LdaModel(corpust_fidf, id2word=dictionary, num_topics=n_topics)
for i in range(0,n_topics):
     temp=lda.show_topic(i,10)
     terms=[]
     for term in temp:
          terms.append(term[1])
          print "Top 10 terms for topic #" + str(i) + ": "+ ", ".join(terms)

