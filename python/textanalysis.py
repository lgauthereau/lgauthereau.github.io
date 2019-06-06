from bs4 import BeautifulSoup
from urllib import request

url = "https://raw.githubusercontent.com/humanitiesprogramming/scraping-corpus/master/full-text.txt"
html = request.urlopen(url).read()
soup = BeautifulSoup(html, 'lxml')
raw_text = soup.text
texts = eval(soup.text)

#print(len(raw_text))
#print(len(texts))

import nltk
from nltk import word_tokenize

tokenized_texts = []
for text in texts:
    tokenized_texts.append(word_tokenize(text))

#for tokenized_text in tokenized_texts:
    #print('=====')
    #print(len(tokenized_text))
    #print(tokenized_text[0:20])

doyle = tokenized_texts[:5]
bronte = tokenized_texts[5:]

# print(len(doyle))
# print(len(bronte))

def normalize(tokens):
    #Takes a list of tokens and returns a list of tokens
    #that has been normalized by lowercasing all tokens and
    #removing Project Gutenberg frontmatter.

#     lowercase all words
    normalized = [token.lower() for token in tokens]

#     very rough end of front matter.
    end_of_front_matter = 90
#     very rough beginning of end matter.
    start_of_end_matter = -2973
#     get only the text between the end matter and front matter
    normalized = normalized[end_of_front_matter:start_of_end_matter]

    return normalized

# print(normalize(bronte[0])[:200])
# print(normalize(bronte[0])[-200:])

doyle = [normalize(text) for text in doyle]
bronte = [normalize(texts) for text in bronte]

#print(doyle[0][:30])

from nltk.corpus import stopwords
#print(stopwords.words('english')[0:30])

def remove_stopwords(tokens):
    return [token for token in tokens if token not in stopwords.words('english')]

#print(len(doyle[0]))
#print('start cleaning')
doyle = [remove_stopwords(text) for text in doyle]
#print('doyle done')
bronte = [remove_stopwords(text) for text in bronte]
#print('bronte done')

#print(len(doyle[0]))

#make a frequency distribution list of a text
example = nltk.FreqDist(doyle[0])
#print(example.most_common(20))

doyle_freq_dist = [nltk.FreqDist(text) for text in doyle]
bronte_freq_dist = [nltk.FreqDist(text) for text in bronte]

def print_top_words(freq_dist_text):
    """Takes a frequency distribution of a text and prints out the top 10 words in it."""
    print('=====')
    print(freq_dist_text.most_common(10))
    print('=====')

# for text in doyle_freq_dist:
#     print_top_words(text)
# for text in bronte_freq_dist:
#     print_top_words(text)

#query particular words, here it's looking for the words holmes and would
#print(doyle_freq_dist[0]['holmes'])
#print(bronte_freq_dist[0]['would'])

def get_counts_in_corpora(token, corpus_one, corpus_two):
    """Take two corpora, represented as lists of frequency distributions, and token query.
    Return the frequency of that token in all the texts in the corpus. The result
    Should be a list of two lists, one for each text."""
    corpus_one_counts = [text_freq_dist[token] for text_freq_dist in corpus_one]
    corpus_two_counts = [text_freq_dist[token] for text_freq_dist in corpus_two]
    return  [corpus_one_counts, corpus_two_counts]

#function that would, given a particular word, return the frequencies of that word in both corpora.
# print(get_counts_in_corpora('evidence', doyle_freq_dist, bronte_freq_dist))
# print(get_counts_in_corpora('reader', doyle_freq_dist, bronte_freq_dist))
# print(get_counts_in_corpora('!', doyle_freq_dist, bronte_freq_dist))
# print(get_counts_in_corpora('?', doyle_freq_dist, bronte_freq_dist))

#can get one list by slicing the other out:
results = get_counts_in_corpora('!', doyle_freq_dist, bronte_freq_dist)
corpus_one_results = results[0]
corpus_two_results = results[1]

# print(corpus_one_results)
# print(corpus_two_results)

nltk.Text(doyle[0]).dispersion_plot(['evidence', 'clue', 'science', 'love', 'say', 'said'])
nltk.Text(bronte[0]).dispersion_plot(['evidence', 'clue', 'science', 'love', 'say', 'said'])
