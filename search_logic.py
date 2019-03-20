from query_parser import queryStringToStemmedList
from search_utils import *
import math
import heapq
from operator import itemgetter

def calculateLength(coordinates):
    i = 0
    for val in coordinates:
        i += val * val
    return math.sqrt(i)

def executeSearch(queryString, term_dict, postings, lengths_file):
    #Load number of docs

    queryTermSet = {}
    queryWeights = {}
    totalNumberOfDocs = getTotalNumberOfDocs(postings)
    queryList = queryStringToStemmedList(queryString)
    scores = {}

    for term in queryList:
        if term not in queryTermSet:
            queryTermSet[term] = [1, getDocFrequency(term, term_dict)]
        else:
            queryTermSet[term][0] += 1

    for term in queryTermSet:
        infoPair = queryTermSet[term]
        if infoPair[1] != 0:
            queryWeights[term] = (1 + math.log10(infoPair[0])) * (math.log10(totalNumberOfDocs/infoPair[1]))

    #Calculating term weights * docId Weights
    for term in queryWeights:
        postingList = loadPostingList(term, term_dict, postings)
        for posting in postingList:
            docId = posting[0]#Depends on the actual position once implemented in the future
            if docId not in scores:
                scores[docId] = 0
            scores[docId] += queryWeights[term] * (1 + math.log10(posting[1]))#Depends on the actual position once implemented(TermFreq in Doc)

    #Normalized scores
    for docId in scores:
        scores[docId] = scores[docId]/getLengthOfDoc(docId, lengths_file)

    topList = heapq.nlargest(10, ([scores[docId], docId] for docId in scores), key = itemgetter(0))
    return [pair[1] for pair in sorted(topList, key = lambda pair: (-pair[0], pair[1]))]
