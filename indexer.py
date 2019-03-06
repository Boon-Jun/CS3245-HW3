import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from os import listdir
from os.path import join, isfile
import pickle
import math

def index(input_directory, output_file_dictionary, output_file_postings):
	# all document ids sorted by id
	doc_ids = [int(d) for d in listdir(input_directory) if isfile(join(input_directory, d))]
	doc_ids.sort()
	# Every term in the dictionary is mapped to a tuple (byte_offset, doc_freq)
	dictionary = {}
	# Every term in the index is mapped to a postings list
	index = {}
	# For every word in every document, add the document_id of the occuring word 
	# to the respective posting list in the index. If word is new, add new key 
	# in dictionary and index
	for doc_id in doc_ids:
		#### Preprocess Text ###
		doc = open(join(input_directory, str(doc_id)), "r")	
		text = doc.read()
		text = text.replace('\n', ' ')
		# tokenize
		sentences = sent_tokenize(text)
		tokens = []
		for sent in sentences:
			tokens.extend([token.lower() for token in word_tokenize(sent)])	
		
		# stem the tokens
		ps = nltk.stem.PorterStemmer()
		stemmed_tokens = [ps.stem(token) for token in tokens]
		for term in stemmed_tokens:
			# strip leading and trailing quotation marks in terms
			if (term.startswith("\"") or term.startswith("'")):
				term = term[1:]
			if (term.endswith("\"" or term.endswith("\'"))):
				term = term[:-1]

			if term not in dictionary:
				dictionary[term] = (None, 1)
				index[term] = [doc_id]
			# if doc_id is not already added to term's postings
			elif index[term][dictionary[term][1]- 1] != doc_id: 
				dictionary[term] = (None, dictionary[term][1] + 1)
				index[term].append(doc_id)
		
	# Add skip pointers to every postings list
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
	offset = postings_file.tell()

	# Write index to postings file and corresponding
        # byte offset to dictionary file
	for k in sorted_terms:
		dictionary[k] = (offset,dictionary[k][1])
		postings_file.write(str(index[k]) + '\n')
		offset = postings_file.tell()
	postings_file.flush()
		
	for term in index:
		print(term)
		print(index[term])

	# Write dictionary to dictionary file			
	dictionary_file = open(output_file_dictionary, "wb")
	pickle.dump(dictionary, dictionary_file)		
	dictionary_file.flush()
	
