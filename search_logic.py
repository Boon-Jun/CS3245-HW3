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

    #Calculates weights for query without normalization
    for term in queryTermSet:
        infoPair = queryTermSet[term]
        if infoPair[1] != 0:
            queryWeights[term] = (1 + math.log10(infoPair[0])) * (math.log10(totalNumberOfDocs/infoPair[1]))

    #Calculates cosine scoring minus the normalization
    for term in queryWeights:
        postingList = loadPostingList(term, term_dict, postings)
        for posting in postingList:
            docId = posting[0]
            if docId not in scores:
                scores[docId] = 0
            scores[docId] += queryWeights[term] * (1 + math.log10(posting[1]))

    #Normalization for docIds
    for docId in scores:
        scores[docId] = scores[docId]/getLengthOfDoc(docId, lengths_file)

    #Retrieve Top 10 Documents with a heap
    topList = heapq.nlargest(10, ([scores[docId], docId] for docId in scores), key = itemgetter(0))
    return [pair[1] for pair in sorted(topList, key = lambda pair: (-pair[0], pair[1]))]
