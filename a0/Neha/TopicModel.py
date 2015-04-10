#!/usr/bin/env python

import praw
import unicodedata
import numpy as np
import lda
import sklearn.feature_extraction.text as text
import StringIO
from sklearn.feature_extraction.text import CountVectorizer
user_agent = ("Neha Desh user agent")
r = praw.Reddit(user_agent=user_agent)
submission = r.get_submission(submission_id='2p3lzc')
flat_comments = praw.helpers.flatten_tree(submission.comments)

documents=[]
for comment in flat_comments:
      if isinstance(comment,praw.objects.MoreComments)==False:
           cms=unicodedata.normalize('NFKD',comment.body).encode('ascii','ignore')
           documents.append(cms)

vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = 'english',   \
                             max_features = 5000) 

train_data_features = vectorizer.fit_transform(documents)
train_data_features = train_data_features.toarray()
vocab=vectorizer.get_feature_names()
model = lda.LDA(n_topics=5, n_iter=200, random_state=1)
model.fit(train_data_features)
topic_word=model.topic_word_
print topic_word
doc_topic=model.doc_topic_
print doc_topic
n = 20
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]
    print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))
import matplotlib.pyplot as plt
print "Comment 1:"
print documents[1]
print "Comment 3:"
print documents[3]
print "Comment 4:"
print documents[4]
print "Comment 8:"
print documents[9]
print "Comment 9:"
print documents[9]




try:
    plt.style.use('ggplot')
except: 
    pass


f, ax= plt.subplots(5, 1, figsize=(8, 8), sharex=True)
for i, k in enumerate([1, 3, 4, 8, 9]):
       ax[i].plot(doc_topic[k,:],'ro')
       ax[i].set_xlim(-1, 21)
       ax[i].set_ylim(0,0.5)
       ax[i].set_ylabel("Prob")
       ax[i].set_title("Document {}".format(k))

ax[4].set_xlabel("Topic")

plt.tight_layout()
plt.show()
