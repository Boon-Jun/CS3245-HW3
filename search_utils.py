import ast

allDocIds = None

def loadPostingList(term, term_dict, postings):
    byteOffset = 0
    try:
        byteOffset = term_dict[term][0]
    except KeyError as e:
        return []
    postings.seek(byteOffset)
    return ast.literal_eval(postings.readline().rstrip())

def getAllDocIds(postings):
    global allDocIds
    if allDocIds == None:
        # Stores the list of all documents once, so that it is not required
        # to load it again
        postings.seek(0)
        allDocIds = ast.literal_eval(postings.readline().rstrip())
    return allDocIds

def getTermCount(term, term_dict):
    try:
        return term_dict[term][1]
    except KeyError as e:
        return 0
