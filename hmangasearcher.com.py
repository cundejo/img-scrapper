"""
Created by Oliver Sosa<oliver@devisfunny.com> on 31/07/17.
Scraping links from http://www.hmangasearcher.com/list/{page}/{lenght}
"""

import os
import urllib
from urllib2 import urlopen, unquote, HTTPError
from urlparse import urljoin, urlparse

from bs4 import BeautifulSoup
from slugify import slugify

INITIAL_URL = 'http://www.hmangasearcher.com/list/1/100'

urlparsed = urlparse(INITIAL_URL)

domain = urlparsed.scheme + '://' + urlparsed.netloc

visited_urls = []


def make_soup(url):
    # url = urllib.unquote(url)  #delete
    try:
        url = urllib.quote(url)
    except KeyError:
        print 'Error encoding the url ' + url
        return None

    url = url.replace('http%3A//', 'http://', 1)

    try:
        print 'Opening url ' + url
        html = urlopen(url).read()
        return BeautifulSoup(html, "html.parser")
    except HTTPError:
        print 'Error: url ' + url + ' not found'
        return None


def get_manga_links(url):
    links = []
    soup = make_soup(url)

    if soup is None:
        return []

    thumbnails = soup.findAll('div', attrs={'class': 'thumbnail'})
    for thumbnail in thumbnails:
        links.append(thumbnail.find('a'))

    return links


def get_manga_chapter_links(manga_url):
    soup = make_soup(manga_url)
    if soup is None:
        return []
    chapter_wrapper = soup.find('div', attrs={'class': 'chlist'})
    return chapter_wrapper.findAll('a')


def get_image_and_pages(chapter_url):
    soup = make_soup(chapter_url)
    if soup is None:
        return []
    pagination_ul = soup.find('ul', attrs={'class': 'pagination'})
    last_link = pagination_ul.find('li', class_="next").find_previous_sibling()
    last_page = last_link.get_text()
    images = soup.select("img.img-rounded.img-responsive.center-block")
    images.append(last_page)
    return images


def save_images(first_img, pages):
    first_img_url_parsed = urlparse(first_img.get('src'))
    (url_path, filename) = first_img_url_parsed.path.rsplit('/', 1)
    path = 'hentai/' + slugify(unquote(url_path))
    try:
        os.makedirs(path)
    except OSError:
        print 'Comic already exist: ' + path
        local_pages = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
        if local_pages == int(pages):
            print "And has all the pages"
            return
        else:
            print "Fuck, some pages missing! Recovering..."

    for page in range(1, int(pages)+1):
        image_url = first_img_url_parsed.scheme + '://' + first_img_url_parsed.netloc + url_path + '/' + str(
            page) + '.jpg'
        filename = path + '/' + str(page) + '.jpg'
        if not os.path.exists(filename):
            print 'Saving ' + filename
            urllib.urlretrieve(image_url, filename)


def run():
    manga_links = get_manga_links(INITIAL_URL)
    for manga_link in manga_links:
        manga_chapter_link = get_manga_chapter_links(urljoin(domain, manga_link.get('href')))
        for chapter_link in manga_chapter_link:
            print '\nStarting with another Comic'
            image_and_quantity_pages = get_image_and_pages(urljoin(domain, chapter_link.get('href')))
            first_img = image_and_quantity_pages[0]
            pages = image_and_quantity_pages[-1]
            save_images(first_img, pages)


run()
#
# a = get_image_and_pages('http://www.hmangasearcher.com/c/34-year-old%20Begging%20Wife/5')
# a = get_image_and_pages('http://libs.loc/a%E2%88%9E%40%23%24%25%5E%26%2A%28%5E/aa.html')
# # b = get_image_and_pages('http://www.hmangasearcher.com/c/34-year-old%20Begging%20Wife/5')
# # c = get_image_and_pages('http://www.hmangasearcher.com/c/3%20Angels%20Short%20-%20Episode%201%20-%20Original%20Work/1')
#
# save_images(a[0], a[-1])
# # save_images(b[0], b[-1])
# # save_images(c[0], c[-1])
