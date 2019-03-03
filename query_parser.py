import re
import nltk
import boolean_operations
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
                    output.append(operatorStack.pop())
                if operatorStack[-1] == '(':
                    operatorStack.pop()
            else:
                while operatorStack and compareOperators(token, operatorStack[-1]) != 1:
                     output.append(operatorStack.pop())
                operatorStack.append(token)
        else:
            output.append(token)
    while operatorStack:
        output.append(operatorStack.pop())
    return output
