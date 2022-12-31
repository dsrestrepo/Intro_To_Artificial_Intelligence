from nltk.tokenize import word_tokenize
import string
import re

import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
    S -> NP VP | S Conj S | VP NP | S PP S | S PP | S NP
    AP -> Adj | Adj AP | Adv
    NP -> N | Det NP | AP NP | N PP | Det AP NP | NP Adv V | AP N | Det N AP
    PP -> P NP | P
    VP -> V | V NP | V NP PP | V PP | Adv V | V AP
"""


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Convert all characters to lowercase
    sentence_lower = sentence.lower()
    # Tokenize the words
    tokenized_words = word_tokenize(sentence_lower)
    # For each word 
    filter_tokens = []
    for token in tokenized_words:
        # Check if is alphanumeric
        if token.isalpha():
            # If is alphanumeric append the token
            filter_tokens.append(token)
    
    return filter_tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # For each subtree 
    for index, subtree in enumerate(tree.subtrees()):
        # Create the list to store the data
        if index == 0:
            subtree_list = []
        # Take the label
        label = subtree.label()
        # See if is NP
        if label == "NP":
            # If is NP append
            subtree_list.append(subtree)

    return subtree_list

'''
def is_np_inside(subtree):
    has_np = False
    for index, subtree_2 in enumerate(subtree.subtrees()):
        if subtree_2.label() == 'NP':
            has_np = True
    return has_np
'''

if __name__ == "__main__":
    main()
