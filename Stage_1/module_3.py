from nltk.stem import *
from nltk.tokenize import word_tokenize
stopwords = ['I', 'a', 'about', 'an', 'are', 'as', 'at', 'be', 'by',
    'com','for', 'from', 'how', 'in', 'is', 'it', 'of', 'on', 'or',
    'that', 'the', 'this', 'to', 'was', 'what', 'when', 'where', 'who',
    'will', 'with','the', 'www', '[', ']', '.', ',', '"', ';', ':', '\'']
stemmer = PorterStemmer()

def stem(word_list):
    for x in range(0, len(word_list)):
        if word_list[x] in stopwords:
            word_list[x] = ''
        else:
            word_list[x] = stemmer.stem(word_list[x])
    while ('' in word_list):
        word_list.remove('')
    return word_list