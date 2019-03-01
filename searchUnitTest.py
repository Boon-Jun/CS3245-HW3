import unittest
import booleanOperations
import queryParser

def compactString(string):
    ''' A utility method that removes all white space'''
    return ''.join(string.split())

class TestQueryParser(unittest.TestCase):
    testString1 = "bill OR Gates AND (vista OR XP) AND NOT mac"
    testString2 = "NOT mac AND bill OR Gates AND (vista OR XP)"
    testString3 = "(bill) OR (Gates AND (vista OR XP)) AND NOT mac"
    testString4 = "NOT (mac AND bill) OR (Gates AND (vista OR XP))"
    testString5 = "NOT (mac AND bill) OR Gates AND (vista OR XP)"

    print queryParser.queryStringToPostFixList(testString1)
    print queryParser.queryStringToPostFixList(testString2)

    def testRemoveRedundantBrackets(self):
        self.assertEqual(compactString(queryParser.simplifyQueryString(self.testString3)), compactString(self.testString1))
        self.assertEqual(compactString(queryParser.simplifyQueryString(self.testString4)), compactString(self.testString5))

class TestBooleanOperations(unittest.TestCase):
    # boolean Operations Test
    list1 = [1, 2, 3, 4, 5, 6, 7, 8]
    list2 = [1, 2, 3, (4, 7), 5, 6, 7, 8]
    list3 = [1, 3, 4, (8, 9), 9]
    list4 = []

    def testAndOp(self):
        self.assertEqual(booleanOperations.andOp(self.list1, self.list1), [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(booleanOperations.andOp(self.list2, self.list3), [1, 3, 4, 8])
        self.assertEqual(booleanOperations.andOp(self.list3, self.list4), [])
        self.assertEqual(booleanOperations.andOp(self.list4, self.list3), [])

    def testOrOp(self):
        self.assertEqual(booleanOperations.orOp(self.list1, self.list1), [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(booleanOperations.orOp(self.list2, self.list3), [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(booleanOperations.orOp(self.list3, self.list4), [1, 3, 4, 8, 9])
        self.assertEqual(booleanOperations.orOp(self.list4, self.list3), [1, 3, 4, 8, 9])

    def testNotOp(self):
        self.assertEqual(booleanOperations.notOp(self.list1, self.list1), [])
        self.assertEqual(booleanOperations.notOp(self.list2, self.list3), [2, 5, 6, 7])
        self.assertEqual(booleanOperations.notOp(self.list3, self.list4), [1, 3, 4, 8, 9])
        self.assertEqual(booleanOperations.notOp(self.list4, self.list3), [])

if __name__ == '__main__':
    unittest.main()
