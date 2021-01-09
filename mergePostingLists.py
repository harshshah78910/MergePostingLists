#!/usr/bin/env python
# coding: utf-8

# In[5]:


import re
import nltk
import collections 
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
#nltk.download("stopwords")
import json


# In[9]:


stop_words = {'a',
 'about',
 'above',
 'after',
 'again',
 'against',
 'ain',
 'all',
 'am',
 'an',
 'and',
 'any',
 'are',
 'aren',
 "aren't",
 'as',
 'at',
 'be',
 'because',
 'been',
 'before',
 'being',
 'below',
 'between',
 'both',
 'but',
 'by',
 'can',
 'couldn',
 "couldn't",
 'd',
 'did',
 'didn',
 "didn't",
 'do',
 'does',
 'doesn',
 "doesn't",
 'doing',
 'don',
 "don't",
 'down',
 'during',
 'each',
 'few',
 'for',
 'from',
 'further',
 'had',
 'hadn',
 "hadn't",
 'has',
 'hasn',
 "hasn't",
 'have',
 'haven',
 "haven't",
 'having',
 'he',
 'her',
 'here',
 'hers',
 'herself',
 'him',
 'himself',
 'his',
 'how',
 'i',
 'if',
 'in',
 'into',
 'is',
 'isn',
 "isn't",
 'it',
 "it's",
 'its',
 'itself',
 'just',
 'll',
 'm',
 'ma',
 'me',
 'mightn',
 "mightn't",
 'more',
 'most',
 'mustn',
 "mustn't",
 'my',
 'myself',
 'needn',
 "needn't",
 'no',
 'nor',
 'not',
 'now',
 'o',
 'of',
 'off',
 'on',
 'once',
 'only',
 'or',
 'other',
 'our',
 'ours',
 'ourselves',
 'out',
 'over',
 'own',
 're',
 's',
 'same',
 'shan',
 "shan't",
 'she',
 "she's",
 'should',
 "should've",
 'shouldn',
 "shouldn't",
 'so',
 'some',
 'such',
 't',
 'than',
 'that',
 "that'll",
 'the',
 'their',
 'theirs',
 'them',
 'themselves',
 'then',
 'there',
 'these',
 'they',
 'this',
 'those',
 'through',
 'to',
 'too',
 'under',
 'until',
 'up',
 've',
 'very',
 'was',
 'wasn',
 "wasn't",
 'we',
 'were',
 'weren',
 "weren't",
 'what',
 'when',
 'where',
 'which',
 'while',
 'who',
 'whom',
 'why',
 'will',
 'with',
 'won',
 "won't",
 'wouldn',
 "wouldn't",
 'y',
 'you',
 "you'd",
 "you'll",
 "you're",
 "you've",
 'your',
 'yours',
 'yourself',
 'yourselves'} 
ps = PorterStemmer()


# In[10]:


file = open("testData.txt","r",encoding="utf8")


# In[11]:


f = file.readlines()
print(f)


# In[20]:


docId=''
docText=''
mapp = {}
for eachLine in f:
    split = eachLine.split("\t")
    docId = split[0]
    docId = int(docId)
    docText = split[1]
    
    processedText = preprocessText(docText)
    
    whiteSpaceToken = processedText.split(" ")
    
    for token in whiteSpaceToken:
        if token not in stop_words:
            stem_token = ps.stem(token)
            if stem_token not in mapp:
                docList = [docId]
                mapp.__setitem__(stem_token, docList)
            else:
                docList=mapp.__getitem__(stem_token)
                docList.append(docId)
                sorted(docList)


# In[21]:


finalMap = {}
for token in mapp:
    tempList = mapp.__getitem__(token)
    llist = LinkedList()
    finalMap.__setitem__(token, llist)
    for docId in tempList:
        llist.insert(docId)


# In[22]:


def preprocessText(txt):
    txt = txt.lower()
    txt = removeSpecialCharacters(txt)
    txt = removeWhiteSpaces(txt)
    txt = txt.strip()
    return txt


# In[23]:


def removeWhiteSpaces(tk):
    return re.sub(' +', ' ', tk)


# In[24]:


def removeSpecialCharacters(tk):
    return re.sub('[^A-Za-z0-9]+', ' ', tk)


# In[25]:


preprocessText('is hydroxychloroquine effective?')


# In[26]:


finalMapp = {}
with open("sample_res.json", "w") as p:
    finalMapp.__setitem__("postingsList", mapp)
    json.dump(finalMapp,p, indent=1)


# In[27]:


class Node:
    
    next=None
    
    def __init__(self, data):
        self.data = data
        self.next = None


# In[28]:


class LinkedList:
    
    def __init__(self):
        self.head=None
        self.length = 0
    
    def insert(self,data):
        if(self.head == None):
            node = Node(data)
            self.head = node  
        else:
            node = Node(data)
            temp = self.head
            while temp.next is not None:
                temp = temp.next
            temp.next=node
        self.length = self.length + 1
                    


# In[2]:


llist = LinkedList()


# In[13]:


llist.insert(21)


# In[14]:


llist.length


# In[227]:


temp = llist.head
while temp is not None:
    print(temp.data)
    temp = temp.next


# In[29]:


queryFile = open("testQuery.txt","r",encoding="utf8")
qf = queryFile.readlines()
queryPostingMap = {}
for eachLine in qf:
    queryPreProcessText = preprocessText(eachLine)
    querySplits = queryPreProcessText.split(" ")
    queryTokens = []
    for i in querySplits:
        if i not in stop_words:
            stem_token = ps.stem(i)
            queryTokens.append(stem_token)
            if(stem_token not in queryPostingMap):
                linkedList = finalMap.__getitem__(stem_token)
                queryPostingMap.__setitem__(stem_token, linkedList)
    print(queryTokens)


# In[30]:


queryFile.close()


# In[32]:


queryPostingMap


# In[ ]:




