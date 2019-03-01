from booleanOperations import notOp, andOp
from searchUtils import *

class CombinedTerm():
    """Cache query terms that have common boolean operation
       for lazy calculation. """
    def __init__(self, operation):
        self.operation = operation
        self.termsList = []

    def addNewTerm(self, term):
        self.termsList.append(term)

    def getOperation(self):
        return self.operation

    def getTerms(self):
        return self.termsList

    def sortTermsList(self, term_dict):
        termCounts = []
        for term in self.termsList:
            if isinstance(term, CombinedTerm):
                termCounts.append(1e9)
            elif type(term) is list:
                return len(term)
            else:
                termCounts.append(getTermCount(term, term_dict))
        termsList = [terms for _,terms in sorted(zip(termCounts,self. termsList))]

    def mergeCombinedTerm(self, combinedTerm):
        if isinstance(combinedTerm, CombinedTerm) and combinedTerm.operation == self.operation:
            self.termsList.extend(combinedTerm.termsList[:])
        else:
            print "Invalid combinedTerm merging"

    def computeCombinedTerm(self, term_dict, postings, primaryList = None):
        intermediateList = primaryList

        self.sortTermsList(term_dict)

        if self.operation == "and":
            for term in self.termsList:
                if isinstance(term, CombinedTerm):
                    intermediateList = term.computeCombinedTerm(term_dict, postings, intermediateList)
                else:
                    operand = term if type(term) is list else loadPostingList(term, term_dict, postings)
                    if intermediateList is None:
                        intermediateList = operand
                    else:
                        intermediateList = andOp(operand, intermediateList)
            return intermediateList

        elif self.operation == "not":
            term = self.termsList[0]
            operand = None
            if isinstance(term, CombinedTerm):
                operand = term.computeCombinedTerm(term_dict, postings)
            elif type(term) is list:
                operand = term
            else:
                operand = loadPostingList(term, term_dict, postings)
            return notOp(getFullDict(), operand) if intermediateList is None else notOp(intermediateList, operand)

        else:
            print "InvalidCombinedTerm"
            return []
