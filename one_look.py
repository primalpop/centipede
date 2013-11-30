from bs4 import BeautifulSoup
import re
import urllib2
import json
import sys
import pdb

output = {}

def extractor(cat, cat_url):
	cat_soup = BeautifulSoup(urllib2.urlopen(cat_url).read())
	list_of_words = cat_soup.find_all(href=re.compile("/?loc=rescb&refclue"))
	for keyword in list_of_words:
			s = keyword.contents[0]
			output[cat].append(s.encode('ascii','ignore'))


def builder(categories):
	count = 101
	for cat in categories:
		cat_search_url = 'http://www.onelook.com/?w=*&loc=revfp2&clue=' + cat 
		output[cat] = []
		extractor(cat, cat_search_url)
		cat_next_url = 'http://www.onelook.com/?w=*:%s&ws1=1&first='%cat
		while(count < 500):
			cat_next_url = cat_next_url + str(count)
			extractor(cat, cat_next_url)
			count += 100

if __name__=="__main__":
	categories = ['health', 'weather', 'crime', 'employment']
	builder(categories)
	with open('categories.json', 'w') as outfile:
  		json.dump(output, outfile)

#http://www.onelook.com/?w=*:health&ws1=1&first=101
#http://www.onelook.com/?w=*&loc=revfp2&clue=health