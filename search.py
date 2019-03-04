#!/usr/bin/python
import re
import nltk
import sys
import getopt
import pickle
import search_logic
import time

def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"

dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)

queriesFile = open(file_of_queries, "r")
outputFile = open(file_of_output, "w")
term_dict = pickle.load(open(dictionary_file, "rb"))
postings = open(postings_file, "r")

initialTime = time.time()

for query in queriesFile:
    #resultsList = search_logic.executeBasicSearch(query, term_dict, postings)
    resultsList = search_logic.executeOptimizedSearch(query, term_dict, postings)
    if type(resultsList) is list:
        outputFile.write(', '.join(str(docId) for docId in resultsList) + '\n')
    else:
        outputFile.write('\n')
print "Execution Time: " + str(time.time() - initialTime) + "s"
