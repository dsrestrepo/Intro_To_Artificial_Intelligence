import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probabilities = {}
    page_links = len(corpus[page])
    total_pages = len(corpus)

    # If the page doesn't have links all links have the same probability
    if not page_links:
        for html in corpus:
            probabilities[html] = 1 / total_pages
        return probabilities

    # If tha page have links:
    # Calculate the probability given by 1 - damping factor for each link 
    for html in corpus:
        probabilities[html] = (1 - damping_factor) / total_pages
    # Add to damping probability the link probability:
    for link in corpus[page]:
        probabilities[link] = probabilities[link] + damping_factor / page_links

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Choose random rage to start using the index
    index = random.randint(0, len(corpus.keys()) - 1)

    # Get initial page
    list_pages = corpus.keys()
    list_pages = list(list_pages)
    initial_page = list_pages[index]

    pages_count = {}

    # Take n samples
    for i in range(0, n):
        # Mark page as selected
        if (not(pages_count)):
            pages_count[initial_page] = 1
        elif (not (initial_page in pages_count)):
            pages_count[initial_page] = 1
        else:
            pages_count[initial_page] = pages_count[initial_page] + 1 
        # Take other page using the transition model:
        pages_prob = transition_model(corpus, initial_page, damping_factor)
        probability = random.random()
        # For each page
        for page in pages_prob.keys():
            # If the probability of the page is upper go directly to that page
            if pages_prob[page] > probability:
                initial_page = page
                break
            # If the probability is more than the first link
            if probability > pages_prob[page]:
                # Use a lower probability
                probability = probability - pages_prob[page]

    # Normalization factor
    factor = 1.0 / sum(pages_count.values())
    normalized_distribution = {k: v*factor for k, v in pages_count.items()}

    print(f'The final distribution of sample rank is: {normalized_distribution}')
    print(f'the sum of values is {sum(normalized_distribution.values())}')

    return normalized_distribution


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Constants
    threshold = 0.001
    total_pages = len(corpus.keys())
    # Initial rank is the same for all pages
    initial_distribution = 1.0/total_pages
    pages_distribution = {page: initial_distribution for page in corpus.keys()}

    # Start itraltion till convergence
    convergence = False
    while not(convergence):
        count_pages = 0
        # for each page:
        for html in corpus:
            # damping probability
            random_page_prob = (1 - damping_factor) / total_pages
            # for each page
            for i, page in enumerate(corpus):
                # Get the number of elemnts linked to that page
                num_links = len(corpus[page])
                if i == 0:
                    factor = 0
                # See just the pages that are linked
                if html in corpus[page]:
                    # Add the probability of that link
                    factor = factor + pages_distribution[page] / num_links
            # Calculate the factor asociated tho that page
            factor = damping_factor * factor
            # Add to the probability
            random_page_prob = random_page_prob + factor
            # If the difference is less than the threshhold
            if abs(pages_distribution[html] - random_page_prob) < threshold:
                # The rank for that page has been calculated
                count_pages = count_pages + 1
            # Add rank
            pages_distribution[html] = random_page_prob 
        if count_pages == total_pages:
            convergence = True

    # Normalization factor
    factor = 1.0 / sum(pages_distribution.values())
    normalized_distribution = {k: v*factor for k, v in pages_distribution.items()}

    
    print(f'The final distribution of iterate rank is: {normalized_distribution}')
    print(f'the sum of values is {sum(normalized_distribution.values())}')

    return normalized_distribution


if __name__ == "__main__":
    main()
