from bs4 import BeautifulSoup
import re
import urllib2
import json
import sys
import pdb
import requests
from pprint import pprint


output, data = {}, {}

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

def build_wiki_words(location):
    loc_url = 'http://scrapit.herokuapp.com/q/?q=http://en.wikipedia.org/wiki/' + location
    wiki_results = requests.get(loc_url)
    wiki_words = [word.encode('ascii','ignore') for word in wiki_results.text.split(", ")]
    wiki_words = [word.replace('"','') for word in wiki_words]
    output_values = [y for x in output.keys() for y in output[x]]
    return list(set.intersection(set(wiki_words), set(output_values)))

def read_place_json():
    #import ipdb; ipdb.set_trace()
    with open('city_words.json') as f:
        for line in f:
            pre_data = json.loads(line)
            proc_line = [word.encode('ascii','ignore') for word in pre_data.values()[0]]
            key =  pre_data.keys()[0].encode('ascii','ignore')
            data[key] = proc_line
                    
def write_json():
    with open('categories.json', 'w') as outfile:
        json.dump(output, outfile)          

def compare(location, category):
    s1 = set(data[location])
    s2 = set(build_wiki_words(location.replace(' ', '_')))
    total = set.intersection(s1, s2)
    print len(s1), len(s2), len(total)
    s3 = set(output[category])
    cat_inter = set.intersection(s1, s2, s3)
    s1_inter = set.intersection(s1, s3)
    s2_inter = set.intersection(s2, s3)
    print len(s1_inter), len(s2_inter), len(cat_inter)   


if __name__=="__main__":
    categories = ['health', 'weather', 'crime', 'employment']
    builder(categories)
    read_place_json()
    write_json()
    location = 'cleveland'
    for category in categories:
        print location, category
        compare(location, category)
#http://www.onelook.com/?w=*:health&ws1=1&first=101
#http://www.onelook.com/?w=*&loc=revfp2&clue=health