import re
import nltk
import booleanOperations
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()
operatorPriority = {'not': 2, 'and': 1, 'or': 0, '(': -1}

def isOperator(op):
    return op in operatorPriority or op == ')' or op == "("

def compareOperators(op1, op2):
    if operatorPriority[op1] < operatorPriority[op2]:
        return -1
    elif operatorPriority[op1] == operatorPriority[op2]:
        return 0
    else:
        return 1

def insertSpaceBeforeAndAfterBrackets(queryString):
    pat = re.compile(r"([()])")
    return pat.sub(" \\1 ", queryString)

def removeRedundantBrackets(queryList):
    ''' This method removes all brackets
        that does not have a 'NOT' expression
        immediately preceding it and does not DIRECTLY encloses
        an 'OR' expression.

        That is the 'OR' expression is enclosed
        by the bracket(1), but it is not
        enclosed by another bracket(2) such that
        (1) encloses (2). '''
    hasNotOperator = False
    withinBrackets = False
    validBracket = False
    openBracketPos = -1
    validBracketHistoryStack = []
    invalidBrackets = set()
    for x in range(len(queryList)):
        token = queryList[x]
        if withinBrackets:
            if token == '(':
                validBracketHistoryStack.append((openBracketPos, validBracket))
                if hasNotOperator:
                    validBracket = True
                else:
                    validBracket = False
                openBracketPos = x
            elif token == 'or':
                validBracket = True
            elif token == ')':
                if not validBracket:
                    invalidBrackets.add(openBracketPos)
                    invalidBrackets.add(x)
                if validBracketHistoryStack:
                    top = validBracketHistoryStack.pop()
                    openBracketPos = top[0]
                    validBracket = top[1]
                else:
                    openBracketPos = -1
                    validBracket = False
                    withinBrackets = False
        else:
            if token == '(':
                if hasNotOperator:
                    validBracket = True
                else:
                    validBracket = False
                withinBrackets = True
                openBracketPos = x

        if token == 'not':
            hasNotOperator = True
        else:
            hasNotOperator = False

    output = []
    for x in range(len(queryList)):
        if x not in invalidBrackets:
            output.append(queryList[x])

    return output

def simplifyQueryString(queryString):

    spacedOutString = insertSpaceBeforeAndAfterBrackets(queryString)
    queryList = [word for word in spacedOutString.split()]

    return ' '.join(removeRedundantBrackets(queryList))

def queryStringToPostFixList(queryString):
    #We shall parse with shunting-yard algorithm here
    output = []
    operatorStack = []
    spacedOutString = insertSpaceBeforeAndAfterBrackets(queryString)
    tokenizedString = [word.lower() if isOperator(word) else stemmer.stem(word.lower()) for word in spacedOutString.split()]
    for token in tokenizedString:
        if isOperator(token):
            if token == '(':
                operatorStack.append(token)
            elif token == ')':
                while operatorStack and operatorStack[-1] != '(':
                    output.append(operatorStack[-1])
                    operatorStack.pop()
                if operatorStack[-1] == '(':
                    operatorStack.pop()
            else:
                while operatorStack and compareOperators(token, operatorStack[-1]) != 1:
                     output.append(operatorStack[-1])
                     operatorStack.pop()
                operatorStack.append(token)
        else:
            output.append(token)
    while operatorStack:
        output.append(operatorStack[-1])
        operatorStack.pop()
    return output        
