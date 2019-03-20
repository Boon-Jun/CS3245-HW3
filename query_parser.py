import re
import nltk
import boolean_operations
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

def insertSpaceBeforeAndAfterBrackets(queryString):
    pat = re.compile(r"([()])")
    return pat.sub(" \\1 ", queryString)

def queryStringToStemmedList(queryString):

    #TODO?: REMOVE QUOTES FROM QUERY?
    return [stemmer.stem(word.lower()) for word in queryString.split()]
