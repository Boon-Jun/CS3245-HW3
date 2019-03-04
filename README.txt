This is the README file for A0000000X's submission

== Python Version ==

I'm (We're) using Python Version <2.7.1 or replace version number> for
this assignment.

== General Notes about this assignment ==

Indexing Algorithm:
Searching Algorithm:
The query is first parsed from infix to postfix notation with the help of shunting-yard
algorithm as suggested.

To process the queries, we will be merging the posting lists, 2 terms at a time.
We utilize three different strategies in an attempt to improve
the searching speed of each query. Firstly, skip pointers are implemented, for faster
merges. The skip pointers are implemented in a way such that sqrt(len(posting_list))
will be spaced out evenly over a posting list.

Secondly, the posting list of all documentIds will be cached during the
processing of the queries. This is because retrieving the full list takes a
significant amount of time, and we believe that the list of all documentIds is
probably one of the most retrieved list from postings.txt.

Lastly, we utilized the idea of Lazy Evaluation when evaluating a query.
Each term and a 'NOT' or 'AND' operator is not immediately evaluated to obtain
a list of document IDs.
The reason for lazy evaluation is mainly for the following 2 scenarios.
1) 'NOT x' operations requires the program to merge a list of all document Ids
   with 'NOT x', which is an expensive operation. Processing 'NOT x AND y' together,
   is on the other hand faster as size of list y <= list all Document Ids.
   However, to evaluate 'NOT x AND y', we have to delay the evaluation of NOT x,
   until y has been processed.

2) Not only does processing smaller sets first reduces the size of the posting list that
   needs to be stored in memory, it also reduces computational cost since merging
   smaller sets is faster. Lazy evaluation allows the program to choose the
   smaller term to process first and delaying the evaluation of the larger terms.
   For example, consider 'x AND y AND z' operations such that the size of list z
   is smaller than y and z. It is most optimal to process z first, and lazy evaluation
   ensures that x AND y will not be evaluated until z is processed.

== Files included with this submission ==

index.py - Required file for submission
indexer.py -
dictionary.txt - Pickled dictionary of terms from the Reuters Training Dataset
postings.txt - Postings List of each term specified in dictionary.txt

search.py - Required file for submission
search_logic.py - Main implementation of search logic
query_parser.py - Shunting-yard algorithm to parse infix queries to postfix queries
boolean_operations.py - Implementation of NOT,AND,OR boolean operations
advanced_search.py - Contains 'CombinedTerms' class and its subclasses
search_utils.py - Commonly used utility methods for searching


== Statement of individual work ==

Please initial one of the following statements.

[x] I, A0000000X, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

<Please fill in>

== References ==

Implementation details of shunting-yard algorithm: https://en.wikipedia.org/wiki/Shunting-yard_algorithm
