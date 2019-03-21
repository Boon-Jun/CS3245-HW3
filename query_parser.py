import re
import nltk
import boolean_operations
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

def insertSpaceBeforeAndAfterBrackets(queryString):
    pat = re.compile(r"([()])")
    return pat.sub(" \\1 ", queryString)

def queryStringToTermsList(queryString):

    #Query string will be split and have each individual terms stemmed with PorterStemmer
    return [stemmer.stem(word.lower()) for word in queryString.split()]
