import re
import requests
from bs4 import BeautifulSoup

r = requests.get("http://www.gutenberg.org/ebooks/search/?query=charles+dickens")
html = r.content
soup = BeautifulSoup(html, 'html.parser')

#print(soup.prettify())

items_per_page = soup.find("meta", {"name": "itemsPerPage"})
items = int(items_per_page['content'])

check_next = soup.select("[title^=Nex]")

booklist = []

i = 0

while soup.select("[title^=Nex]") != []:

    review_titles_list = soup.find_all("li", {"class": "booklink"})

    for block in review_titles_list:
        titles = block.find_all("span", {"class": "cell content"})
        for title in titles:
            if title.find("span", {"class": "subtitle"}) != None and re.match('.*?Charles Dickens.*',(title.find("span", {"class": "subtitle"})).get_text()):
                author = (title.find("span", {"class": "subtitle"})).get_text()
                booklist.append(str(i) + ". " + title.find("span", {"class": "title"}).get_text() + " by " + author)
                i += 1

    get_start_index = soup.find("meta", {"name": "startIndex"})
    start_index = int(get_start_index['content']) + items

    r = requests.get("http://www.gutenberg.org/ebooks/search/?start_index="+str(start_index)+"&query=charles+dickens")
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')

r = requests.get("http://www.gutenberg.org/ebooks/search/?start_index="+str(start_index)+"&query=charles+dickens")
html = r.content
soup = BeautifulSoup(html, 'html.parser')
review_titles_list = soup.find_all("li", {"class": "booklink"})

for block in review_titles_list:
    titles = block.find_all("span", {"class": "cell content"})
    for title in titles:
        if title.find("span", {"class": "subtitle"}) != None and re.match('.*?Charles Dickens.*', (title.find("span", {"class": "subtitle"})).get_text()):
            author = (title.find("span", {"class": "subtitle"})).get_text()
            booklist.append(str(i) + ". " + title.find("span", {"class": "title"}).get_text() + " by " + author)
            i += 1

print('[%s]'%'\n'.join(map(str,booklist)))
