import ast

def loadPostingList(term, term_dict, postings):
    byteOffset = 0
    try:
        byteOffset = term_dict[term][0]
    except KeyError as e:
        return []
    postings.seek(byteOffset)
    return ast.literal_eval(postings.readline().rstrip())

def getFullDict(postings):
    postings.seek(0)
    return ast.literal_eval(postings.readline().rstrip())

def getTermCount(term, term_dict):
    try:
        return term_dict[term][1]
    except KeyError as e:
        return 0
