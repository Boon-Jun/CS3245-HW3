import re
import nltk
import boolean_operations
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

# 'operatorPriority' set stores the operator priority,
# required for shunting-yard algorithm.
# Operator priority for '(' and ')' will be implicitly considered
# within the implementation of the algorithm itself, and hence will
# not be stored over here.
operatorPriority = {'not': 2, 'and': 1, 'or': 0}

def isOperator(op):
    return op in operatorPriority or op == ')' or op == "("

def compareOperators(op1, op2):
    if op1 not in operatorPriority or op2 not in operatorPriority:
        return -1
    if operatorPriority[op1] < operatorPriority[op2]:
        return 1
    else:
        return 0

def insertSpaceBeforeAndAfterBrackets(queryString):
    pat = re.compile(r"([()])")
    return pat.sub(" \\1 ", queryString)

def queryStringToPostFixList(queryString):
    # Query string will be parsed from infix to postfix notation with
    # shunting-yard algorithm
    output = []
    operatorStack = []

    #Adds spaces before and after brackets to make string tokenization simpler
    spacedOutString = insertSpaceBeforeAndAfterBrackets(queryString)

    tokenizedString = [word.lower() if isOperator(word) else stemmer.stem(word.lower()) for word in spacedOutString.split()]

    for token in tokenizedString:
        if isOperator(token):
            if token == '(':
                operatorStack.append(token)
            elif token == ')':
                # Remove all operators from operatorStack until '(' is found
                while operatorStack and operatorStack[-1] != '(':
                    output.append(operatorStack.pop())
                if operatorStack[-1] == '(':
                    operatorStack.pop()
            else:
                # Remove any operators from the top of the operator stack if
                # the current token has a strictly higher priority.
                while operatorStack and compareOperators(token, operatorStack[-1]) == 1:
                     output.append(operatorStack.pop())
                operatorStack.append(token)
        else:
            output.append(token)
    while operatorStack:
        output.append(operatorStack.pop())
    return output
