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
    out = {}
    c_links = len(corpus)
    p_links = len(corpus[page])
    base = (1-damping_factor)/c_links

    if p_links == 0:
        for link in corpus:
            out[link] = 1/c_links
        return out

    for link in corpus[page]: # Bad that I count repeating links multiple times?
        if link in out:
            out[link] += 1
        else:
            out[link] = 1

    for link in corpus:
        if link in out:
            out[link] = out[link]/p_links * damping_factor + base
        else:
            out[link] = base
    
    return out



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    out = {}

    current = random.choice(list(corpus.keys()))

    for i in range(n):
        if current in out:
            out[current] += 1
        else:
            out[current] = 1
        
        next = transition_model(corpus, current, damping_factor)

        current = random.choices(list(next.keys()), weights=list(next.values()), k=1)[0]

    for link in corpus:
        if link in out:
            out[link] = out[link]/n
        else:
            out[link] = 0
    
    return out
    
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    out = {}
    buffer = {}
    N = len(corpus)
    flag = True

    for link in corpus:
        out[link] = 1/N

    while flag:
        flag = False
        for link in out:
            p_in = 0
            for i in corpus:
                i_len = len(corpus[i])
                if i_len == 0:
                    p_in += out[i]/N
                elif link not in corpus[i]:
                    continue
                else:
                    p_in += out[i] / i_len
            buffer[link] = (1-damping_factor)/N + p_in * damping_factor
        for key in buffer:
            if round(buffer[key],3) != round(out[key], 3):
                out = buffer.copy()
                flag = True
                break

    return out

if __name__ == "__main__":
    main()
