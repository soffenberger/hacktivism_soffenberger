#! /usr/bin/python

import BeautifulSoup
import urllib2
import lxml.html
import random
import psycopg2 as ps


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


	# Save Links
	d = 0
	g = page_links
	for i in g:
		a = self.get_past_links(i)
		if (a == True):
			page_links[d] = ''
		d +=1
	page_links = filter(None, page_links)

	for i in page_links:
		self.insert_link(i)
		
		

        # Update links 
        self.links = self.links.union( set(page_links) ) 
	
		
        # Choose a random url from non-visited set
        try:
		self.current_page = random.sample( self.links.difference(self.visited_links),1)[0]
        	self.counter+=1
	except ValueError:
		print "nothing new"
		


    def run(self): 
	a = 0
        while (self.visited_links == self.links):
            self.open()

	for link in self.links:
            with open('articles.txt', 'a') as links:
		links.write(link + '\n')
		a+=1
	return a

    def get_past_links(self, link):
	conn = ps.connect("dbname =  'hacktivism'") 
	cur = conn.cursor()
	cur.execute("""SELECT links FROM links where links = '%s'""" %link)
	exists = cur.fetchone()
	if exists:
		return True
	else:
		return False
	conn.commit()
	cur.close()
	conn.close()

    def insert_link(self, link):
	conn = ps.connect("dbname =  'hacktivism'") 
	cur = conn.cursor()
	cur.execute ("""Insert into links values (DEFAULT, '%s')""" %link)
	conn.commit()
	cur.close()
	conn.close()

	

if __name__ == '__main()__':
	self()
	
