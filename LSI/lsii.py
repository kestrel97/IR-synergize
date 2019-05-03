import re
import os
import math
import pickle
import numpy as np
from collections import defaultdict

stopwords = {'a', 'is', 'the', 'of', 'all', 'and', 'to', 'can', 'be', 'as', 'once', 'for', 'at', 'am',
             'are', 'has', 'have', 'had', 'up', 'his', 'her', 'in', 'on', 'no', 'we', 'do', "'"}


def createDictionary():
    doc = 1
    dictionary = {}

    while doc <= 23:  # Because we have got 50 documents
        path = 'cvs/' + str(doc) + '.txt'  # Documents path
        file = open(path, encoding="utf8")
        line = file.readline()
        position = 0

        while line:
            line = line.lower()
            list = re.findall(r"[\w']+", line)  # Returns a list of words
            for token in list:
                position = position + 1
                if token not in stopwords:
                    if token not in dictionary:
                        dictionary[token] = {}
                        dictionary[token]["Doc" + str(doc)] = [position]
                    else:
                        temp = dictionary.get(token)
                        if ("Doc" + str(doc)) not in temp:
                            dictionary[token]["Doc" + str(doc)] = [position]
                        else:
                            dictionary.setdefault(token).setdefault("Doc" + str(doc)).append(position)
            line = file.readline()

        doc = doc + 1
        file.close()

    return dictionary



exsistIn = os.path.isfile('Dictionary.pickle')

if exsistIn:
    pickle_in = open("Dictionary.pickle", "rb")
    dictionary = pickle.load(pickle_in)
else:
    print("Creating dictionary, please wait this may take a few seconds...")
    dictionary = createDictionary()
    pickle_out = open("Dictionary.pickle", "wb")
    pickle.dump(dictionary, pickle_out)
    pickle_out.close()

words = list(dictionary)
words = sorted(words)

n = 23  # 50 documents
m = len(words)  # Size of vectors
documents = [[0 for x in range(n)] for y in range(m)]  # 50 vectors for 50 document set

for i in range(0, m):
    for j in range(0, n):
        if ("Doc" + str(j+1)) in dictionary[words[i]]:
            documents[i][j] = len(dictionary[words[i]]["Doc" + str(j+1)])
#print(documents)
a=np.array(documents)
#print(a)
# print(len(a))
# print(len(a[0]))
U, S, V=np.linalg.svd(a, full_matrices=True, compute_uv=True)
# print(U.shape)
# print(S.shape)
# print(V.shape)
c=np.zeros((2,2))
c[0][0]=S[0]
c[1][1]=S[1]

print(c)

#query
query=defaultdict()
file=open('JDI.txt')
data=file.read().replace('\n', " ").replace("--"," ").replace("."," ").replace("-"," ").replace("/"," ")
word=[]
for term in words:
    query[term]=0

for token in data.lower().split(" "):

    if token=='':
        continue

    x=re.findall("[a-zA-Z]",token)
    term=''.join(x)
    if term in words:
        query[term]=int(query[term])+1
query=dict((sorted(query.items())))
querry=[]
for term in words:
    querry.append(int(query[term]))
#print(querry)

#result eval
Uprime=U[:,[0,1]]
print(Uprime.shape)
Vprime=V[:,[0,1]]
print(Vprime.shape)
d=Vprime.transpose()
print(d.shape)

qprime=np.array(querry)
f=qprime.transpose()
print(qprime.shape)

temp=f.dot(Uprime)
qpp=temp.dot(np.linalg.inv(c))
# print(qpp)

result=defaultdict()
# print(d[:,22])
for i in range(n):
    cos = np.dot(qpp, d[:,i]) / (np.linalg.norm(qpp) * np.linalg.norm(d[:,1]))
    result[i+1]=cos
    # print(cos)
result=dict((sorted(result.items())))
print(result)