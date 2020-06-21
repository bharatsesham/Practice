#!/usr/bin/env python3

import nltk
from nltk.tokenize import word_tokenize 
from operator import itemgetter
from nltk.stem import WordNetLemmatizer
import sys

new_word_sum = ''
final_items = []

for line in sys.stdin:
	line = str(line)
	new_word_sum = new_word_sum + line

new_word_sum = nltk.word_tokenize(new_word_sum)
text = nltk.Text(new_word_sum)

words = [w.lower() for w in text if w.isalpha()]

lemmatizer = WordNetLemmatizer()

#new_words = ['$' if word==lemmatizer.lemmatize("sciences") or word==lemmatizer.lemmatize('seas') or word==lemmatizer.lemmatize('fire') else word for word in words]

new_words = ['$' if lemmatizer.lemmatize(word)=="science" or lemmatizer.lemmatize(word)=='sea' or lemmatizer.lemmatize(word)=='fire' else word for word in words]


tgs = nltk.trigrams(new_words)

for item in tgs:
	if '$' in item:
		print(item)







   
