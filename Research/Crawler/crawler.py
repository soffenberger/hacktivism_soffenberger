import BeautifulSoup
import urllib2
import lxml.html
import random


class Crawler(object):
    """docstring for Crawler"""

    def __init__(self, current_page, xpath):

        self.tree= None                   # Beautiful Soup object
        self.current_page = current_page           # Current page's address
        self.links          = set() # Queue with every links fetched
        self.visited_links  = set()
	self.link_xpath	= xpath	    #xpath link

        self.counter = 0 # Simple counter for debug purpose

    def open(self):

        # Open url
        print self.counter , ":", self.current_page
        self.tree  = lxml.html.parse(self.current_page)
        self.visited_links.add(self.current_page) 

        # Fetch every links
        page_links = []
        try :
            page_links = self.tree.xpath(self.link_xpath)
        except Exception: # Magnificent exception handling
            pass

        # Update links 
        self.links = self.links.union( set(page_links) ) 

        # Choose a random url from non-visited set
        self.current_page = random.sample( self.links.difference(self.visited_links),1)[0]
        self.counter+=1


    def run(self):
	a = 0
        # Crawl 3 webpages (or stop if all url has been fetched)
        while (self.visited_links == self.links):
            self.open()

	for link in self.links:
            with open('articles.txt', 'a') as links:
		links.write(link + '\n')
		a+=1
	return a
	

if __name__ == '__main()__':
	self()
	
