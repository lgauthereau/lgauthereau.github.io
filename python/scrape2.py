# get the libraries we need
import nltk
from bs4 import BeautifulSoup
from urllib import request

# stored the url we're using
url = "https://github.com/humanitiesprogramming/scraping-corpus"

# look inside the library and use request to go to the designated url and read/get the html from it
html = request.urlopen(url).read()

# take the html and turn it into a "soup" object.
soup = BeautifulSoup(html, 'lxml')
our_text = soup.text
# a is all the anchors in the html code
links = soup.find_all('a')[0:10]

# use slice to limit what you get back
#print(our_text[0:2000])
# look for every new line, ie line spaces, \n, and replace with a single space
#print(soup.text.replace('\n', ' '))

links_html = soup.select('td.content a')
this_link = links_html[0]

print(this_link['href'])
urls = []
# take each link and make a new list with processed urls
for link in links_html:
# need create what to_append means, need to get rid of blob and replace with nothing
    to_append = link['href'].replace('blob/', '')
# need to add the beginning of the url
    urls.append("https://raw.githubusercontent.com" + to_append)
#this will pull out a single url, the 4th url in the list
test_url = urls[3]
corpus_texts = []

for url in urls:
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    text = soup.text.replace('\n', '')
    corpus_texts.append(text)
    print("Scraping " + url)

print(len(corpus_texts))
print(len(corpus_texts[0]))

this_text = corpus_texts[0]
# The novel we got was a massive string. This asks the machine to break it up
process_this_text = nltk.word_tokenize(this_text)
print(process_this_text[0:20])
# The 50 most commonly used words and their distribution
print(nltk.FreqDist(process_this_text).most_common(50))
