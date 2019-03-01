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

def executeOptimizedSearch(queryString, term_dict, postings):

    postfixList = queryStringToPostFixList(queryString)

    operandsStack = []

    for x in range(len(postfixList)):
        item = postfixList[x]
        if item == 'not':
            operand = operandsStack.pop()
            newCombinedTerm = CombinedTerm("not")
            newCombinedTerm.addNewTerm(operand)
            operandsStack.append(newCombinedTerm)
        elif item == 'and':
            operand1 = operandsStack.pop()
            operand2 = operandsStack.pop()
            finalOperand = None

            if isinstance(operand1, CombinedTerm) and operand1.getOperation() == "and":
                finalCombinedTerm = operand1.addNewTerm(operand2)
            elif isinstance(operand2, CombinedTerm) and operand2.getOperation() == "and":
                finalCombinedTerm = operand2.addNewTerm(operand1)
            else:
                finalCombinedTerm = CombinedTerm("and")
                finalCombinedTerm.addNewTerm(operand1)
                finalCombinedTerm.addNewTerm(operand2)
            operandsStack.append(finalCombinedTerm)

        elif item == 'or':
            operand1 = operandsStack.pop()
            operand2 = operandsStack.pop()

            if isinstance(operand1, CombinedTerm):
                operand1 = operand1.computeCombinedTerm(term_dict, postings)
            elif type(operand1) is not list:
                operand1 = loadPostingList(operand1, term_dict, postings)

            if isinstance(operand2, CombinedTerm):
                operand2 = operand2.computeCombinedTerm(term_dict, postings)
            elif type(operand2) is not list:
                operand2 = loadPostingList(operand2, term_dict, postings)

            operandsStack.append(orOp(operand1, operand2))
        else:
            operandsStack.append(item)
    if len(operandsStack) == 1:
        if isinstance(operandsStack[0], CombinedTerm):
            return operandsStack[0].computeCombinedTerm(term_dict, postings)
        else:
            return operandsStack[0]
    else:
        print("Invalid Query")
