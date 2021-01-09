#! python3

import re
import sys
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download("stopwords")
import json

class Node:
    next = None

    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:

    def __init__(self):
        self.head = None
        self.length = 0

    def insert(self, data):
        if (self.head == None):
            node = Node(data)
            self.head = node
        else:
            node = Node(data)
            temp = self.head
            while temp.next is not None:
                temp = temp.next
            temp.next = node
        self.length=self.length+1


def preprocessText(txt):
    txt = txt.lower()
    txt = removeSpecialCharacters(txt)
    txt = removeWhiteSpaces(txt)
    txt = txt.strip()
    return txt

def removeWhiteSpaces(tk):
    return re.sub(' +', ' ', tk)

def removeSpecialCharacters(tk):
    return re.sub('[^A-Za-z0-9]+', ' ', tk)


def invokeMergeOperationForQuery(queryTokens, finalMap):
    postingToLengthMap = {}
    tempPostingList = {}
    for token in queryTokens:
        tempLinkedList = finalMap.__getitem__(token)
        tempPostingList.__setitem__(token,tempLinkedList)
        postingToLengthMap.__setitem__(token, tempLinkedList.length)
    #print(postingToLengthMap)
    #result = mergeTwoPostings(finalMap.__getitem__('clinic'),finalMap.__getitem__('covid'))
    #print(result[0] , result[1])
    totalNumberOfComparison = 0;
    finalResult = None
    while postingToLengthMap.__len__() != 1:
        l = sortTheMapBasedOnValue(postingToLengthMap)
        t1 = l[0][0]
        t2 = l[1][0]
        p1 = tempPostingList.__getitem__(t1)
        p2 = tempPostingList.__getitem__(t2)
        postingToLengthMap.pop(t1)
        postingToLengthMap.pop(t2)
        result = mergeTwoPostings(p1, p2)
        totalNumberOfComparison = totalNumberOfComparison + result[1]
        postingToLengthMap.__setitem__(t1+t2, result[0].length)
        tempPostingList.__setitem__(t1+t2,result[0])
        finalResult = result[0]


    #print(postingToLengthMap,totalNumberOfComparison, finalResult)

    tempList = []
    if(finalResult is not None):
        head = finalResult.head
        while head is not None:
            tempList.append(head.data)
            head = head.next

    return tempList,totalNumberOfComparison


def sortTheMapBasedOnValue(postingToLengthMap):
    return sorted(postingToLengthMap.items(), key=lambda kv: (kv[1], kv[0]))

def mergeTwoPostings(llist1, llist2):

    temp=[]
    noOfComparison=0
    head1 = llist1.head
    head2 = llist2.head
    while head1 is not None and head2 is not None:
        noOfComparison = noOfComparison + 1
        if(head1.data == head2.data):
            temp.append(head1.data)
            head1 = head1.next
            head2 = head2.next
        elif head1.data > head2.data:
            head2 = head2.next
        else:
            head1 = head1.next

    llist = LinkedList()
    for docId in temp:
        llist.insert(docId)

    return llist,noOfComparison


def populatePostingList(stem_token, postingListMap, linkedList):
    tempList = []
    head = linkedList.head
    while head is not None:
        tempList.append(head.data)
        head = head.next
    postingListMap.__setitem__(stem_token,tempList)


def main():
    input_file = str(sys.argv[1])
    output_file = sys.argv[2]
    query_file = sys.argv[3]
    #input = sys.argv
    #print(input)
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    file = open(input_file, "r", encoding="utf8")
    f = file.readlines()
    docId = ''
    docText = ''
    mapp = {}
    for eachQuery in f:
        split = eachQuery.split("\t")
        docId = split[0]
        docId = int(docId)
        docText = split[1]

        processedText = preprocessText(docText)

        whiteSpaceToken = processedText.split(" ")

        for token in whiteSpaceToken:
            if token not in stop_words:
                stem_token = ps.stem(token)
                if stem_token not in mapp:
                    docList = set()
                    docList.add(docId)
                    mapp.__setitem__(stem_token, docList)
                else:
                    docList = set(mapp.__getitem__(stem_token))
                    docList.add(docId)
                    sortedList = sorted(docList)
                    mapp.__setitem__(stem_token,sortedList)
    finalMap = {}

    for token in mapp:
        tempList = mapp.__getitem__(token)
        llist = LinkedList()
        finalMap.__setitem__(token, llist)
        for docId in tempList:
            llist.insert(docId)
    #print(finalMap)

    queryFile = open(query_file, "r", encoding="utf8")
    qf = queryFile.readlines()
    formattedResult = {}
    postingListMap ={}
    daatMap = {}
    for eachQuery in qf:
        queryPreProcessText = preprocessText(eachQuery)
        querySplits = queryPreProcessText.split(" ")
        queryTokens = []
        for i in querySplits:
            if i not in stop_words:
                stem_token = ps.stem(i)
                queryTokens.append(stem_token)
                if (stem_token not in postingListMap):
                    linkedList = finalMap.__getitem__(stem_token)
                    populatePostingList(stem_token,postingListMap,linkedList)
        #print(queryTokens)
        result = invokeMergeOperationForQuery(queryTokens,finalMap)
        resultsMap = {}
        resultsMap.__setitem__("results", result[0])
        resultsMap.__setitem__("num_docs",result[0].__len__())
        resultsMap.__setitem__("num_comparisons", result[1])
        eachQuery = eachQuery.strip()
        daatMap.__setitem__(eachQuery,resultsMap)

    formattedResult.__setitem__("postingsList", postingListMap)
    formattedResult.__setitem__("daatAnd" , daatMap)

    with open(output_file, "w") as p:
        json.dump(formattedResult,p)

if __name__=="__main__":
    main()
