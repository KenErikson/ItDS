# coding=utf-8
## all imports
from IPython.display import HTML
import numpy as np
import urllib2
import bs4 #this is beautiful soup
import time
import operator
import socket
import cPickle
import re # regular expressions

from pandas import Series
import pandas as pd
from pandas import DataFrame

import matplotlib
import matplotlib.pyplot as plt
#%matplotlib inline

import seaborn as sns
# sns.set_context("talk")
# sns.set_style("white")

# u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
#
# users = pd.read_csv(
#     'http://files.grouplens.org/datasets/movielens/ml-100k/u.user',
#     sep='|', names=u_cols)
#
# print(users.head())
#url = 'http://www.crummy.com/software/BeautifulSoup'
BASE_URL = 'https://www.yelp.se'
ORIGINAL_URL = BASE_URL + '/search?find_loc=Kaivokatu+1,+helsinki&start=0&cflt=breakfast_brunch&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2'
# source = urllib2.urlopen(ORIGINAL_URL).read()
# root_search_soup = bs4.BeautifulSoup(source,'html.parser')



#https://www.yelp.se/search?find_loc=Kaivokatu+1,+helsinki&start=0&cflt=breakfast_brunch&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2&open_time=9300
#https://www.yelp.se/search?find_loc=Kaivokatu+1,+helsinki&start=0&cflt=breakfast_brunch&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2

TOTAL_RESULTS_PER_PAGE = 30
CURRENT_OFFSET = 0

##
#Get result count
##
# total_results_contents = root_search_soup.find("span",{"class": "pagination-results-window"}).contents[0]
# av_index = total_results_contents.index('av')
#
# total_results = int(total_results_contents[av_index+2:].strip())
# print 'Total results: ' + str(total_results)
#
# number_of_pages = total_results/TOTAL_RESULTS_PER_PAGE
# if total_results % TOTAL_RESULTS_PER_PAGE != 0:
#     number_of_pages +=1
# print 'Number of pages: ' + str(number_of_pages)

##
# Loop over every search result on every page
##
# hrefs_to_resturants = []
# for i in range(number_of_pages):
#     url = ORIGINAL_URL.replace("start=0", "start=" + str(i * TOTAL_RESULTS_PER_PAGE))
#     print url
#     source = urllib2.urlopen(url).read()
#     root_search_soup = bs4.BeautifulSoup(source, 'html.parser')
#     print 'Handling page Nr.' + str(i+1)
#     search_result_divs = root_search_soup.findAll("div", {"class": "search-result"})
#     print search_result_divs
#     print str(len(search_result_divs)) + ' results on this page'
#     # Loop over every search result
#     results_handled_count=0
#     for restaurant_div in search_result_divs:
#         results_handled_count += 1
#         # Check if 5 reviews
#         over_4_reviews = False
#         element = restaurant_div.find("span", {"class": "review-count"})
#         if element is not None:
#              element_text = element.text
#              element_review_index=element_text.index(' recension')
#              review_count = int(element_text[:element_review_index])
#              if review_count >= 5:
#                  over_4_reviews = True
#
#         if over_4_reviews:
#             restaurant_a = restaurant_div.find("a", {"class": "biz-name"})
#             hrefs_to_resturants.append(restaurant_a.get('href'))
#
#     print 'Handled ' + str(results_handled_count) + ' results on page ' + str(i+1)
# print 'Got a total of ' + str(len(hrefs_to_resturants)) + ' viable results'
# print hrefs_to_resturants

hrefs_to_resturants = [u'/biz/sis-deli-ja-cafe-helsinki-2', u'/biz/la-torrefazione-helsinki', u'/biz/karl-fazer-caf%C3%A9-helsinki-2', u'/biz/factory-helsinki-5', u'/biz/fleuriste-helsinki', u'/biz/caf%C3%A9-engel-helsinki-2', u'/biz/caf%C3%A9-daja-helsinki', u'/biz/bakers-helsinki', u'/biz/deli-cafe-maya-helsinki', u'/biz/ursula-helsinki', u'/biz/tin-tin-tango-helsinki', u'/biz/cargo-helsinki-2', u'/biz/piritta-helsinki', u'/biz/birgitta-helsinki', u'/biz/ipi-kulmakuppila-helsinki', u'/biz/moko-market-helsinki', u'/biz/cardemumma-helsinki-2', u'/biz/siltanen-helsinki', u'/biz/mille-mozzarelle-helsinki', u'/biz/sis-deli-ja-cafe-helsinki-3', u'/biz/sandro-helsinki-2', u'/biz/hima-ja-sali-helsinki-3', u'/biz/dylan-helsinki-10']


##
# Check each of the viable restaurants
##
for href in hrefs_to_resturants:
    print 'Testing ' +href
    url = BASE_URL + href
    source = urllib2.urlopen(url).read()
    root_restaurant_soup = bs4.BeautifulSoup(source, 'html.parser')

    # Check takes credit card
    element = root_restaurant_soup.find("div", {"class":"short-def-list"})
    if element is not None:
        attribute_text = element.find("dt").text.strip()
        if "Tar betalkort" not in attribute_text:
            continue

    # Check open at least once during Saturday/Sunday
    open_weekend = False
    element = root_restaurant_soup.find("table",{"class":"hours-table"})
    tbody = element.find("tbody")
    for trow in tbody.findChildren("tr"):
        #print trow.findChild("th").text
        if u"lör" in trow.findChild("th").text or u"sön" in trow.findChild("th").text:
            #print trow.findChild("th")
            #print trow.findChild("td")
            if len(trow.findChild("td").findChildren("span"))>0:
                open_weekend = True
                print "YES"
                break

    if not open_weekend:
        print "Not open on weekends"
        continue
    print "Open on weekends"

    #Get Distance
    #Get Rating
    #Get Review Count
    #Get prices
