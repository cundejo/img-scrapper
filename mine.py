import os
import urllib
from urllib2 import urlopen
from urlparse import urljoin

from bs4 import BeautifulSoup

INITIAL_URL = 'http://rule34c.paheal.net/books/'

visited_urls = []


def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "html.parser")


def get_links(url):
    soup = make_soup(url)
    return [link for link in soup.findAll('a')]


def is_url_of_image(url):
    res = url.split('/')[-1]
    ext = res.split('.')[-1]
    if ext.lower() in ['jpg', 'jpeg', 'gif', 'png']:
        return True
    return False


def get_image(url, path):
    print "Saving img from %s to %s" % (url, path + url.split('/')[-1])
    filename = os.path.join(path, url.split('/')[-1])
    urllib.urlretrieve(url, filename)


def recursive(url, path=None):
    if url in visited_urls:
        print "URL already visited"
        return
    else:
        visited_urls.append(url)

        if not is_url_of_image(url):
            if not path:
                print "Creating first path"
                path = url.split('/')[-1].split('.')[0] or url.split('/')[-2]
                try:
                    os.makedirs(path)
                except OSError:
                    pass

            else:
                path += '/' + (url.split('/')[-1].split('.')[0] or url.split('/')[-2])
                try:
                    os.makedirs(path)
                except OSError:
                    print "Folder already exists"
                    return

        if is_url_of_image(url):
            print "Getting image"
            get_image(url, path)
        else:
            print "Getting more pages"
            links = get_links(url)
            for link in links:
                if link.get('href') != u'../':
                    recursive(urljoin(url, link.get('href')), path)


def run():
    recursive(INITIAL_URL)


run()
