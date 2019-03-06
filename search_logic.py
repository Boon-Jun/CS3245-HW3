from query_parser import *
from boolean_operations import *
from search_utils import *
from advanced_search import *

def executeBasicSearch(queryString, term_dict, postings):

    # This method is a basic implementation of boolean search operations
    # with very minimal optimization. This is not used in the actual execution of
    # the search, but it is used for comparison with more optimized algorithm
    # to ensure some "correctness" in the optimized search

    #Converts infix query string to list in postfix notation
    postfixList = queryStringToPostFixList(queryString)

    operandsStack = []

    #Process the query after converting it to postfix notation
    for x in range(len(postfixList)):
        item = postfixList[x]
        if item == 'not':
            operand = operandsStack.pop()
            if type(operand) is not list:
                operand = loadPostingList(operand, term_dict, postings)
            operandsStack.append(notOp(getAllDocIds(postings), operand))
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
            # If item is not a boolean operator than it is an operand

            # strip leading and trailing quotation marks if any in operand
            if (item.startswith("\"") or item.startswith("'")):
                token = token[1:]
            if (item.endswith("\"" or item.endswith("\'"))):
                token = token[:-1]
            operandsStack.append(item)
    if len(operandsStack) == 1:
        if type(operandsStack[0]) is not list:
            # To account for cases where no boolean operations are executed, this
            # loads the relevant posting list and remove all skip pointers.
            return [item[0] if type(item) is tuple else item for item in loadPostingList(operandsStack[0], term_dict, postings)]
        else:
            return operandsStack[0]
    else:
        print("Invalid Query")

def executeOptimizedSearch(queryString, term_dict, postings):

    #Converts infix query string to list in postfix notation
    postfixList = queryStringToPostFixList(queryString)
    operandsStack = []

    #Process the query after converting it to postfix notation
    for x in range(len(postfixList)):
        item = postfixList[x]
        if item == 'not':
            operand = operandsStack.pop()

            # "CombinedTerm" simply stores the 'NOT' operator and operand together
            # as one "term". This is because NOT x itself is expensive to
            # compute, and delaying this computation can possibly allow the
            # program to find a more optimal way to compute this term after a
            # "larger chunk" of the query has been processed.
            # e.g Processing NOT x AND y together is better than processing
            # z = (NOT x) first and then y AND z since we can work with
            # smaller postings list.)

            operandsStack.append(NotCombinedTerm(operand))
        elif item == 'and':
            operand1 = operandsStack.pop()
            operand2 = operandsStack.pop()
            finalOperand = None

            # "CombinedTerm" stores the 'AND' operator and all relevant operands
            # together as one "term".
            # The argument is similar to the above, as delaying the calculation
            # of 'AND' operation, allows the program to process a "larger chunk"
            # of the query, before deciding which sets to merge first.
            # e.g Consider  the query 'x AND y AND z'. Suppose that both x and y
            # has a size of 30000, and z has a size of 1. Performing y AND z first
            # is better than performing x AND y first since y AND z has a maximum
            # size of 1 while x AND y has a maximum size of 30000.

            if isinstance(operand1, AndCombinedTerm):
                finalCombinedTerm = operand1.addNewTerm(operand2)
            elif isinstance(operand2, AndCombinedTerm):
                finalCombinedTerm = operand2.addNewTerm(operand1)
            else:
                finalCombinedTerm = AndCombinedTerm(operand1).addNewTerm(operand2)
            operandsStack.append(finalCombinedTerm)

        elif item == 'or':
            operand1 = operandsStack.pop()
            operand2 = operandsStack.pop()

            # If the next boolean operation to execute is the 'OR' operation,
            # the program will compute all CombinedTerms since all other boolean
            # operations have a higher or equal priority than the 'OR' operation,
            # and has to be computed before this 'OR' operation can be evaluated.
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
            # If item is not a boolean operator than it is an operand

            # strip leading and trailing quotation marks if any in operand
            if (item.startswith("\"") or item.startswith("'")):
                token = token[1:]
            if (item.endswith("\"" or item.endswith("\'"))):
                token = token[:-1]
            operandsStack.append(item)

    if len(operandsStack) == 1:
        if isinstance(operandsStack[0], CombinedTerm):
            #Compute the combined term before output.
            return operandsStack[0].computeCombinedTerm(term_dict, postings)
        elif type(operandsStack[0]) is not list:
            # To account for single term queries without boolean operations, this
            # loads the relevant posting list and remove all skip pointers.
            return [item[0] if type(item) is tuple else item for item in loadPostingList(operandsStack[0], term_dict, postings)]
        else:
            return operandsStack[0]
    else:
        print("Invalid Query")
