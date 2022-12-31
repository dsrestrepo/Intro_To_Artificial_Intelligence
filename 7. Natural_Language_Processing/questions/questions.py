import nltk
from nltk.tokenize import word_tokenize
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    corpus_dic = {}
    # for each file in the directory
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        # Check if is a .txt
        if path[-4:] == '.txt':
            # Then read the file
            with open(path, "r", encoding="utf-8") as text_doc:
                #print(text_doc.read())
                # Write the doc in the value
                corpus_dic[file] = text_doc.read()
    #print(corpus_dic)
    return corpus_dic


    

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Convert all characters to lowercase
    document_lower = document.lower()
    # Tokenize the words
    tokenized_words = word_tokenize(document_lower)

    tokenized_filtered = []
    # For each token
    for token in tokenized_words:
        # If is punctuation or in stopwords ignore
        if (token in string.punctuation) or (token in nltk.corpus.stopwords.words("english")):
            #print(token)
            continue
        # If not in punctuation or stopwords add to list
        else:
            #print(token)
            tokenized_filtered.append(token) 

    return tokenized_filtered


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Calculate N: # of docs
    N = len(documents)

    # Take Unique Words
    words = {}
    # For each possible document:
    for file in documents:
        # Take the corpus
        corpus = documents[file]
        # For each word
        for word in corpus:
            # If word is unique
            if word not in words:
                words[word] = 0

    # Calculate document Frequency:
    # For each word
    for word in words:
        # Take each document corpus
        for document in documents:
            corpus = documents[document]
            # Check if word is in corpus
            if word in corpus:
                # If word is in corpus add 1
                words[word] = words[word] + 1
         
    #print(set(words.values()))
    # Calculate tf_idf
    # For each item in dict
    for word in words:
        #calulate the tf-idf using the document Frequency and N
        words[word] = math.log(N/words[word])

    #print(words)
    return words



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idf = {}
    # For each file do:
    for file in files:
        # Take the words
        corpus = files[file]
        tf_idf[file] = 0
        # for each word in queri calculate the tf-idf
        for word in query:
            # If word in query is not in the corpus of file ignore
            if word not in corpus:
                continue
            #print(f'the idf for {word} is: {idfs[word]}')
            # update the tf-idf
            tf_idf[file] = tf_idf[file] + (corpus.count(word) * idfs[word])
            #print(f'The TF-IDF in {file} is: {tf_idf[file]}')
    
    # Then sort using the TF-IDF and save the filenames in that order
    sorted_tf_idf = [file for file, tf_idf in sorted(tf_idf.items(), key=lambda dict_item: dict_item[1], reverse=True)]

    #print(sorted_tf_idf)
    # Top n files:
    top_n = sorted_tf_idf[:n]

    return top_n
    


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    top_sentences = {}
    #for each sentence
    for sentence in sentences:
        # Take the corpus
        corpus = sentences[sentence]
        # Dictionary will store ('matching word measure', 'word density')
        top_sentences[sentence] = [0, 0]
        # For each word in the Query
        for word in query:
            # If word of query is not in corpus ignore
            if word not in corpus:
                continue
            # If is in corpus calculate the 'matching word measure'
            top_sentences[sentence][0] = top_sentences[sentence][0] + idfs[word]
            
            # Count how many times the word is in the sentence
            top_sentences[sentence][1] = top_sentences[sentence][1] + corpus.count(word)
            #print(f'words are {top_sentences[sentence][1]}')
        
        # Calculate the density
        try: 
            top_sentences[sentence][1] = top_sentences[sentence][1] / len(corpus)
        except:
            # Sentence is empty
            top_sentences[sentence][1] = 0
        #print(f'The scores sentences for {sentence} are: {top_sentences[sentence]}')

    # Then sort using both scores and save the filenames in that order
    sorted_sentences = [sentence for sentence, scores in sorted(top_sentences.items(), key=lambda dict_item: (dict_item[1][0], dict_item[1][1]), reverse=True)]

    # Top n files:
    top_n = sorted_sentences[:n]

    return top_n



if __name__ == "__main__":
    main()
