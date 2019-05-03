import nltk

from nltk.stem import PorterStemmer
from nltk import word_tokenize,sent_tokenize,pos_tag
stemmer=PorterStemmer()
file = open('JDI.txt') #open file
lines = file.read() #read all lines
sentences = nltk.sent_tokenize(lines) #tokenize sentences
nouns = [] #empty to array to hold all nouns

for sentence in sentences:
     for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
         
        word=word.lower()
        word=stemmer.stem(word)
        
        if word in nouns:
            None
        else:
            nouns.append(word)

print(nouns)
jd=nouns
nouns.clear()
path = 'cvs/23.txt'  # Documents path
file = open(path, encoding="utf8")
lines = file.read() #read all lines
sentences = nltk.sent_tokenize(lines) #tokenize sentences
nouns = [] #empty to array to hold all nouns

for sentence in sentences:
     for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
        word=word.lower()
        word=stemmer.stem(word)
         
        if word in nouns: 
            None
        else:
            nouns.append(word)
print(nouns)

i=0
for term in nouns:
    if term in jd:
        i+=1
print('Matched noun: ',i)