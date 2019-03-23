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

Before the documents are being ranked, the query string will be split and then stemmed
with PorterStemmer. Further processing is done whereby the leading and trailing quotation
marks is removed from each term to align with how the terms in the documents were processed.

The documents will then be ranked according to the lnc.ltc ranking scheme.
That is to say that the weights of each term in the document will be calculated as :
(1 + log10(term_frequency_in_documents))
whereas the weights of each term in the query will be calculated as:
tf-idf = (1 + log(term_frequency_in_query)) * log(number_of_documents/document_frequency)
After that, cosine normalization will be applied to the weights of each term in both
the query and the document, and the dot product of the weights of the terms in the
query and the weights of the terms in the documents will give us a score.

However, in our actual implementation, we omit the step of computing the cosine
normalization for the query since the computation of the cosine normalization
for the query will reduce the calculated scores by the same factor, and the
actual ranking of the documents will not be affected regardless of the computation.

To retrieve the Top 10 Ranked documents, we utilize python's heapq library, which helps
us create the heap and select the top 10 documents in O(NLog10) time, whereby
N is the number of documents that has matching stems to the query.

In the event that 2 documents have the same score, they will be then be sorted by
their documentIds in ascending order.

== Essay Questions ==

1. In this assignment, we didn't ask you to support phrasal queries, which is a feature that is typically supported in web search engines. Describe how you would support phrasal search in conjunction with the VSM model. A sketch of the algorithm is sufficient. (For those of you who like a challenge, please go ahead and implement this feature in your submission but clearly demarcate it in your code and allow this feature to be turned on or off using the command line switch "-x" (where "-x" means to turn on the extended processing of phrasal queries). We will give a small bonus to submissions that achieve this functionality correctly).

2. Describe how your search engine reacts to long documents and long queries as compared to short documents and queries. Is the normalization you use sufficient to address the problems (see Section 6.4.4 for a hint)? In your judgement, is the ltc.lnc scheme (n.b., not the ranking scheme you were asked to implement) sufficient for retrieving documents from the Reuters-21578 collection?

3. Do you think zone or field parametric indices would be useful for practical search in the Reuters collection? Note: the Reuters collection does have metadata for each article but the quality of the metadata is not uniform, nor are the metadata classifications uniformly applied (some documents have it, some don't). Hint: for the next Homework #4, we will be using field metadata, so if you want to base Homework #4 on your Homework #3, you're welcomed to start support of this early (although no extra credit will be given if it's right).

== Files included with this submission ==
README.txt - This file

index.py - Required file for submission
indexer.py - Perfoms the indexing of directory of documents.
dictionary.txt - Pickled dictionary of terms from the Reuters Training Dataset
postings.txt - Postings List of each term specified in dictionary.txt
lengths.txt - Stores the document length
search.py - Required file for submission
            Usage of search.py now slightly differs from the original due to the
						addition of lengths.txt file
						As such, the correct usage of search.py file will now be:
						python search.py -d dictionary-file -p postings-file -l length-file -q file-of-queries -o output-file-of-results
search_logic.py - Main implementation of search logic
query_parser.py - Contains simple query parser to split and stem a query string
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
