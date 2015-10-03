#! /usr/bin/python


import requests
from progressbar import ProgressBar, Percentage, Bar, ETA
from time import sleep
from lxml import html
import psycopg2
import nltk
from crawler import Crawler

def monthToNum(date):	
	return{
        'January ' : 1,
        'Febuary' : 2,
        'March' : 3,
        'April' : 4,
        'May' : 5,
        'June' : 6,
        'July' : 7,
        'August' : 8,
        'September' : 9, 
        'October' : 10,
        'November' : 11,
        'December' : 12
}[date]

def get_urls_from_text():
	with open ('articles.txt','r') as attack_links:
		lines = attack_links.read().split('\n')
		prbl = len(lines)
		lines.pop(prbl-1)
		return lines

def get_html_from_website(l_url):
	page = requests.get(l_url)
	tree = html.fromstring(page.text)
	return tree

def store_htmls_in_list():
	urls = get_urls_from_text()
	widget = ['Getting link html: ', Percentage(), Bar(), ETA(), ' ']
	pbar = ProgressBar(widgets=widget, maxval=100).start()
	i=0
	html = []
	for l_url in urls:
		url = l_url.encode("ascii")
		html.append(get_html_from_website(url))				
		sleep(0.001)
        	pbar.update(i)
		i+=1
	pbar.finish()
	return html	

def parse_hacker_spot(tree):
	title = tree.xpath('//*[contains(@id,"post")]/header/h1[contains(@class, "entry-title")]/text()')
	time = tree.xpath('//*[contains(@id,"post")]/header/div[2]/div[1]/span[1]/a/time')
	article = tree.xpath('//*[contains(@id, "post")]/div/p')
	print title[0] 
	for i in article:
		print i.text 
	global conn
	cur = conn.cursor()
	temp = time[0].text.split(' ')
	month = temp[0]
	day = temp[1].replace(',','')
	year = temp[2]
	num_month = monthToNum(month)
	timestamp = year + '-' + str(num_month) + '-' + str(day)
	print timestamp
	print("Parsed Hacker Spot")

def parse_crypto_sphere(tree):
	title = tree.xpath('//*[contains(@id,"post")]/h1[contains(@class, "posttitle")')
	time = tree.xpath('//*[contains(@id,"post")]/p/a/time')
	article = tree.xpath('//*[constains(@id,"post")]/section/p[1]')
	print title[0] 
	for i in article:
		print i.text 
	global conn
	cur = conn.cursor()
	temp = time[0].text.split(' ')
	month = temp[0]
	day = temp[1].replace(',','')
	year = temp[2]
	num_month = monthToNum(month)
	timestamp = year + '-' + str(num_month) + '-' + str(day)
	print timestamp
	print("Parsed Crypto Sphere Anon Spot")
		

##def parse_cyber_war_zone(tree):

##def parse_zero_security(tree):

def fill_addresses():
	c = Crawler('http://thehackerspost.com/category/hacking-news', '//*[contains(@id,"post")]/header/h2/a/@href')
	s = c.run()
	r = Crawler('http://thecryptosphere.com/category/anonymous/', '//*[contains(@id,"post")]/div[2]/h2/a/@href')
	g = r.run()
	h = Crawler('http://cyberwarzone.com/category/cyberwar-news/', '//*[contains(@id,"post")]/h5/a/@href')
	f = h.run()
	results = [s,g,f]
	return results

def clean_addresses():
	open('articles.txt', 'w').close()


def main():
	global conn
	conn = psycopg2.connect("dbname = 'hacktivism'")
	cur = conn.cursor()
	results = fill_addresses()
	html_list = store_htmls_in_list()
	for k in range(0,results[0],1):
		parse_hacker_spot(html_list[k])
	for k in range(0,results[1],1):
		parse_crypto_sphere(html_list[1])
	for k in range(0,results[2],1):
		print k	

	conn.commit()
	cur.close()
	conn.close()
	clean_addresses()

	
	


if __name__ == '__main__':
	main()
		
