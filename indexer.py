import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from os import listdir
from os.path import join, isfile
import pickle
import math

def index(input_directory, output_file_dictionary, output_file_postings):
	doc_ids = [d for d in listdir(input_directory) if isfile(join(input_directory, d))]
	doc_ids.sort(key=lambda a: int(a))
	# Every term in the dictionary is mapped to a tuple (byte_offset, doc_freq)
	dictionary = {}
	# Every term in the index is mapped to a postings list
	index = {}
	# For every word in every document, add the document_id of the occuring word 
	# to the respective posting list in the index. If word is new, add new key 
	# in dictionary and index
	for doc_id in doc_ids:
		# tokenize the text in document
		doc = open(join(input_directory, doc_id), "r")	
		text = doc.read()
		sentences = [sentence for sentence in sent_tokenize(text)]
		tokens = []
		for sent in sentences:
			tokens.extend([token for token in word_tokenize(sent)])	
		# stem the tokens
		ps = nltk.stem.PorterStemmer()
		stemmed_tokens = [ps.stem(token) for token in tokens]
		for term in stemmed_tokens:
			if term not in dictionary:
				dictionary[term] = (None, 1)
				index[term] = [doc_id]
			# if doc_id is not already added to term's postings
			elif index[term][dictionary[term][1]- 1] != doc_id: 
				dictionary[term] = (None, dictionary[term][1] + 1)
				index[term].append(doc_id)

	# Add skip pointers to every posting
	for term in index:
		doc_freq = dictionary[term][1]
		skip_pointers_count = int(math.sqrt(doc_freq))
		skip_size = int(doc_freq / skip_pointers_count)
		for i in range(0, (doc_freq - skip_size - 1)):
			if i % skip_size == 0:
				index[term][i] = (index[term][i], i + skip_size)

	# Write dictionary and index
	offset = 0
	postings_file = open(output_file_postings, "w")
	sorted_terms = dictionary.keys()
	sorted_terms.sort()
	
	# Write all document ids at top of postings file
	postings_file.write(str(doc_ids) + '\n')	
	
	# Write index to postings file and corresponding
        # byte offset to dictionary file
	for k in sorted_terms:
		postings_file.write(str(index[k]) + '\n')
		dictionary[k] = (offset,dictionary[k][1])
		offset = postings_file.tell()
	postings_file.flush()
	
	for k in sorted_terms:
		print(k + " " + str(dictionary[k]))

	# Write dictionary to dictionary file			
	dictionary_file = open(output_file_dictionary, "wb")
	pickle.dump(dictionary, dictionary_file)		
	dictionary_file.flush()
	
print(index("/home/a/ananda96/CS3245-HW2/test_docs","test_dictionary.txt", "test_postings.txt"))
'''input_directory = "/home/a/ananda96/CS3245-HW2/test_docs"
print(isfile(join(input_directory, "2")))
doc_ids = [d for d in listdir(input_directory) if isfile(join(input_directory, d))]
print(doc_ids)'''