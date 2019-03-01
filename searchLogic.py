from queryParser import *
from booleanOperations import *
from searchUtils import *
from AdvancedSearch import CombinedTerm

def executeBasicSearch(queryString, term_dict, postings):
    #Just a placeHolder to retrieve for full dictionary listings
    fullDict = getFullDict()

    postfixList = queryStringToPostFixList(queryString)

    operandsStack = []

    for x in range(len(postfixList)):
        item = postfixList[x]
        if item == 'not':
            operand = operandsStack.pop()
            if type(operand) is not list:
                operand = loadPostingList(operand, term_dict, postings)
            operandsStack.append(notOp(fullDict, operand))
        elif item == 'and':
            operand1 = operandsStack.pop()
            operand2 = operandsStack.pop()
            if type(operand1) is not list:
                operand1 = loadPostingList(operand1, term_dict, postings)
            if type(operand2) is not list:
                operand2 = loadPostingList(operand2, term_dict, postings)
            operandsStack.append(andOp(operand1, operand2))
        elif item == 'or':
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
