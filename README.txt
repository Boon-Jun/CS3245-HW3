This is the README file for A0000000X-***REMOVED***'s submission

== Python Version ==

I'm (We're) using Python Version <2.7.1 or replace version number> for
this assignment.

== General Notes about this assignment ==

Indexing Algorithm:
--------------------

Indexing is done in- memory first and then written into the file at the very end.
The postings are stored in a dictionary with the terms are the keys and a list of postings is the value to each term. 
The dictionary of terms is stored in a dicitonary with the terms as the keys and the 
tuple of (byte_offset, document_frequency) as the values. 

The documents are indexed as follows:

1) Document Ids in the directory are are parsed to integers and sorted

2) Preprocess the text in each document. 
	i) Prepare the text by replacing '\n' characters in text with ' '
	ii) Apply the NLTK sentence tokenizer followed by word tokenizer
	iii) Case fold each token
	iv) Apply the NLTK Porter Stemmer
	v) Remove leading and trailing quotation marks (This was done to normalize the terms which were incorrectly 
	tokenized with the apostrophe by the tokenizer. Such tokens are common in speech where the sentence is wrapped in apostrophes)	

3) For each term, if the term is new, add the term to the dictionary and the postings. 
Then add the occuring Document Id (if it has not already been added) into the corresponding 
postings list in the postings and update the document frequency in the dictionary.

3) Then, add approximately sqrt(document_frequency) evenly spaced skip pointers 
to every postings list in the postings, in the form of an index to a document_id to its right, 
accompanying the select Document Ids. Document Ids with skip pointers will be tuples 
of the form: (document_id, skip_index). This way, an entire posting list can be loaded as a python list
when searching and skips will be performed by accessing the element in the list at the specified skip index.

4) Write the list of sorted Document Ids to the top of the postings file. This will be used
for NOT queries. 

5) While writing the postings list for each term in the postings file, fill the byte_offset value of
where it is written in the file from the start, in each corresponding term in the dictionary. This 
makes finding the postings list to be loaded into the memory more efficient, during the search.

6) Pickle the dictionary and write the it to the dictionary file. The entire dictionary can
be unpickled in the memory during the search as it is relatively small compared to the postings,
which will only be loaded list by list for every search query.

Searching Algorithm:
---------------------

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


== Essay Questions ==
1) You will observe that a large portion of the terms in the dictionary are numbers. However, we normally do not use numbers as query terms to search. Do you think it is a good idea to remove these number entries from the dictionary and the postings lists? Can you propose methods to normalize these numbers? How many percentage of reduction in disk storage do you observe after removing/normalizing these numbers?
	Ans: We do not think that it is a good idea to remove these number entries from the dictionary and the postings list. This is because the user might request documents which have numbers accompanied by a term (eg. 2008 AND recession). In this case taking the presence of a specific number (year) in the query will return more relevant set of documents. Perhaps the important or frequently occuring numbers such as days months or years can be indexed separately with separate postings list for each. The remaining numbers can then be grouped into the terms Integers and Decimals.

2) What do you think will happen if we remove stop words from the dictionary and postings file? How does it affect the searching phase?

	Ans: Removing stop words will decrease the disk space used tremenously as words such as "the", "It" etc. are present in almost every document. It will not affect the searching phase much unless the user specifically requests for special documents without the stop words perhaps to get documents with uncommon sentence structures (eg. documents with primarily numbers)

3) The NLTK tokenizer may not correctly tokenize all terms. What do you observe from the resulting terms produced by sent_tokenize() and word_tokenize()? Can you propose rules to further refine these results?

	Ans: There are many terms produced by the tokenizers which are often appended or prepended with special symbols as a result of incorrect tokenization of sybols such as apostrophes and hyphens from english words. We tackled this problem in the indexing phase by removing leading and trailing apostrophes specifically as this was the most common case of incorrect tokenization. This is a result of the relative abundance of direct speech and direct citations in the documents. Another case that we did not tackle is acronyms which are often tokenized to individual letters. This can perhaps be prevented by detecting terms with multiple "." in close proximity. 

== Files included with this submission ==

index.py - Required file for submission
indexer.py - Perfoms the indexing of directory of documents.
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

[x] I, A0000000X-***REMOVED***, certify that I have followed the CS 3245 Information
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

We refered to the forums on IVLE to analyze the various ways to implement the indexing and searching.
Implementation details of shunting-yard algorithm: https://en.wikipedia.org/wiki/Shunting-yard_algorithm
