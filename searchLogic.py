import ast
from queryParser import *
from booleanOperations import *

def loadPostingList(term, term_dict, postings):
    byteOffset = 0
    try:
        byteOffset = term_dict[term][0]
    except KeyError as e:
        return []
    postings.seek(byteOffset)
    return ast.literal_eval(postings.readline().rstrip())


def executeSearch(queryString, term_dict, postings):
    #Just a placeHolder to retrieve for full dictionary listings
    fullDict = [x for x in range(1,10000)]

    postfixList = queryStringToPostFixList(queryString)

    operandsStack = []

    for x in range(len(postfixList)):
        item = postfixList[x]
        if item == 'NOT':
            operand = operandsStack.pop()
            if type(operand) is not list:
                operand = loadPostingList(operand, term_dict, postings)
            operandsStack.append(notOp(fullDict, operand))
        elif item == 'AND':
            operand1 = operandsStack.pop()
            operand2 = operandsStack.pop()
            if type(operand1) is not list:
                operand1 = loadPostingList(operand1, term_dict, postings)
            if type(operand2) is not list:
                operand2 = loadPostingList(operand2, term_dict, postings)
            operandsStack.append(andOp(operand1, operand2))
        elif item == 'OR':
            operand1 = operandsStack.pop()
            operand2 = operandsStack.pop()
            if type(operand1) is not list:
                operand1 = loadPostingList(operand1, term_dict, postings)
            if type(operand2) is not list:
                operand2 = loadPostingList(operand2, term_dict, postings)
            operandsStack.append(orOp(operand1, operand2))
        else:
            operandsStack.append(item)
    if len(operandsStack) == 1:
        return operandsStack[0]
    else:
        print("Invalid Query")
