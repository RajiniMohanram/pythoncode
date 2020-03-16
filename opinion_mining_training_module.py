import nltk
import xml.etree.ElementTree as ET
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
import sys
import progress_bar
import time
from pandas import DataFrame
import matplotlib.pyplot as plt

all_words = []

def create_word_features(words):
	global all_words
	return dict([(word.lower(), True) for word in words if len(word) > 2 and word in all_words])

def sentiment_analysis(all_reviews):
    time.sleep(2)
    print("\n\nTraining the algorithm with review dataset...")
    time.sleep(2)
    root = ET.parse('set1.xml').getroot()
    reviews = []
    sentiment = []

    for item in root.findall('.//Motivation'):
    	reviews.append(item.text)

    for item in root.findall('.//Sentiment'):
    	sentiment.append(item.text)

	
    positive_reviews = []
    negative_reviews = []
    neutral_reviews = []
	
    global all_words
	
    for i in range(0, len(reviews)):
    	if sentiment[i] == None or reviews[i] == None:
    		continue
    	if sentiment[i] == 'positive' :
    		positive_reviews.append(reviews[i])
    	elif sentiment[i] == 'negative' :
    		negative_reviews.append(reviews[i])
    	else :
    		neutral_reviews.append(reviews[i])

    progress_bar.progress(10, 100)

    with open('emoji.txt', 'r',encoding ="utf8") as file:
    	for line in file:
    		line = line.split()
    		emo = ""
    		for subset in range(0, len(line) - 1):
    			emo += line[subset]
    		if line[len(line) - 1] == '1':
    			positive_reviews.append(emo)
    		else:
    			negative_reviews.append(emo)

    progress_bar.progress(33.33, 100)

    root = ET.parse('set2.xml').getroot()

    reviews = []
    sentiment = []

    for item in root.findall('.//Motivation'):
    	reviews.append(item.text)

    for item in root.findall('.//Sentiment'):
    	sentiment.append(item.text)

    for i in range(0, len(reviews)):
    	if sentiment[i] == None or reviews[i] == None:
    		continue
    	if sentiment[i] == 'positive' :
    		positive_reviews.append(reviews[i])
    	elif sentiment[i] == 'negative' :
    		negative_reviews.append(reviews[i])
    	else :
    		neutral_reviews.append(reviews[i])
    for arr in positive_reviews:
    	for word in word_tokenize(arr):
    		all_words.append(word.lower())

    for arr in negative_reviews:
    	for word in word_tokenize(arr):
    		all_words.append(word.lower())

    for arr in neutral_reviews:
    	for word in word_tokenize(arr):
    		all_words.append(word.lower())

    all_words = nltk.FreqDist(all_words)
    all_words = list(all_words.keys())[:550]

    progress_bar.progress(66.66, 100)

    positive_reviews = [(create_word_features(word_tokenize(word)), 'positive') for word in positive_reviews]
    negative_reviews = [(create_word_features(word_tokenize(word)), 'negative') for word in negative_reviews]
    neutral_reviews = [(create_word_features(word_tokenize(word)), 'neutral') for word in neutral_reviews]

    training_set = positive_reviews + negative_reviews + neutral_reviews

    classifier = NaiveBayesClassifier.train(training_set)

    progress_bar.progress(100.0, 100, True)

    time.sleep(1)

    neg = 0
    pos = 0
    neu = 0
    pos_gr=[]
    neg_gr=[]
    neu_gr=[]
    for sentence in all_reviews:
    	sentiment = classifier.classify(create_word_features(word_tokenize(sentence)))
    	if(sentiment == 'negative'):
    		neg += 1
    		neg_gr.append(neg)
    		pos_gr.append(pos)
    		neu_gr.append(neu)
    	elif(sentiment == 'positive'):
    		pos += 1
    		pos_gr.append(pos)
    		neu_gr.append(neu)
    		neg_gr.append(neg)
    	else:
    		neu += 1
    		neu_gr.append(neu)
    		pos_gr.append(pos)
    		neg_gr.append(neg)

    neg += (neu/50)

    total = neg + pos
    if total == 0:
    	print("Mixed reviews...")
    	sys.exit
    data = {'Positive':pos_gr,'Negative':neg_gr,'Neutral':neu_gr}
    df = DataFrame(data,columns=['Positive','Negative','Neutral'])
    
    ax = plt.gca()
    df.plot(kind='line',y='Positive',color='red',ax=ax)
    #plt.show()
    df.plot(kind='line',y='Negative',color='blue',ax=ax)
    #plt.show()
    df.plot(kind='line',y='Neutral',color='black',ax=ax)
    plt.show()
    print("\n\nPositive reviews =", (pos/total) * 100)
    print("Negative reviews =", (neg/total) * 100)    