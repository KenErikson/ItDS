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
source = urllib2.urlopen(ORIGINAL_URL).read()
root_search_soup = bs4.BeautifulSoup(source,'html.parser')


#https://www.yelp.se/search?find_loc=Kaivokatu+1,+helsinki&start=0&cflt=breakfast_brunch&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2&open_time=9300
#https://www.yelp.se/search?find_loc=Kaivokatu+1,+helsinki&start=0&cflt=breakfast_brunch&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2

TOTAL_RESULTS_PER_PAGE = 30
CURRENT_OFFSET = 0

##
#Get result count
##
total_results_contents = root_search_soup.find("span",{"class": "pagination-results-window"}).contents[0]
av_index = total_results_contents.index('av')

total_results = int(total_results_contents[av_index+2:].strip())
print 'Total results: ' + str(total_results)

number_of_pages = total_results/TOTAL_RESULTS_PER_PAGE
if total_results % TOTAL_RESULTS_PER_PAGE != 0:
    number_of_pages +=1
print 'Number of pages: ' + str(number_of_pages)

##
# Loop over every search result on every page
##
hrefs_to_resturants = []
for i in range(number_of_pages):
    url = ORIGINAL_URL.replace("start=0", "start=" + str(i * TOTAL_RESULTS_PER_PAGE))
    print url
    source = urllib2.urlopen(url).read()
    root_search_soup = bs4.BeautifulSoup(source, 'html.parser')
    # print 'Handling page Nr.' + str(i+1)
    search_result_divs = root_search_soup.findAll("div", {"class": "search-result"})
    # print search_result_divs
    print str(len(search_result_divs)) + ' results on this page'
    # Loop over every search result
    results_handled_count=0
    for restaurant_div in search_result_divs:
        results_handled_count += 1
        # Check if 5 reviews
        over_4_reviews = False
        element = restaurant_div.find("span", {"class": "review-count"})
        review_count = 0
        if element is not None:
             element_text = element.text
             element_review_index=element_text.index(' recension')
             review_count = int(element_text[:element_review_index])
             if review_count >= 5:
                 over_4_reviews = True

        if over_4_reviews:
            # Find distance
            small_element = restaurant_div.findChildren("small")[1]
            distance = float(small_element.text.strip()[:-2])

            restaurant_a = restaurant_div.find("a", {"class": "biz-name"})
            hrefs_to_resturants.append(restaurant_a.get('href') + "#" + str(distance) + "-" + str(review_count)) #Fastest way to just add the distance to the url

    print 'Handled ' + str(results_handled_count) + ' results on page ' + str(i+1)
print 'Got a total of ' + str(len(hrefs_to_resturants)) + ' viable results'
print hrefs_to_resturants

#hrefs_to_resturants = [u'/biz/sis-deli-ja-cafe-helsinki-2', u'/biz/la-torrefazione-helsinki', u'/biz/karl-fazer-caf%C3%A9-helsinki-2', u'/biz/factory-helsinki-5', u'/biz/fleuriste-helsinki', u'/biz/caf%C3%A9-engel-helsinki-2', u'/biz/caf%C3%A9-daja-helsinki', u'/biz/bakers-helsinki', u'/biz/deli-cafe-maya-helsinki', u'/biz/ursula-helsinki', u'/biz/tin-tin-tango-helsinki', u'/biz/cargo-helsinki-2', u'/biz/piritta-helsinki', u'/biz/birgitta-helsinki', u'/biz/ipi-kulmakuppila-helsinki', u'/biz/moko-market-helsinki', u'/biz/cardemumma-helsinki-2', u'/biz/siltanen-helsinki', u'/biz/mille-mozzarelle-helsinki', u'/biz/sis-deli-ja-cafe-helsinki-3', u'/biz/sandro-helsinki-2', u'/biz/hima-ja-sali-helsinki-3', u'/biz/dylan-helsinki-10']
#hrefs_to_resturants = [u'/biz/sis-deli-ja-cafe-helsinki-2#0.5', u'/biz/la-torrefazione-helsinki#0.4', u'/biz/karl-fazer-caf%C3%A9-helsinki-2#0.5', u'/biz/factory-helsinki-5#0.4', u'/biz/fleuriste-helsinki#0.8', u'/biz/caf%C3%A9-engel-helsinki-2#0.6', u'/biz/caf%C3%A9-daja-helsinki#0.9', u'/biz/bakers-helsinki#0.4', u'/biz/deli-cafe-maya-helsinki#1.2', u'/biz/ursula-helsinki#2.1', u'/biz/tin-tin-tango-helsinki#1.2', u'/biz/cargo-helsinki-2#1.4', u'/biz/piritta-helsinki#1.0', u'/biz/birgitta-helsinki#2.1', u'/biz/ipi-kulmakuppila-helsinki#1.4', u'/biz/moko-market-helsinki#1.5', u'/biz/cardemumma-helsinki-2#1.7', u'/biz/siltanen-helsinki#1.7', u'/biz/mille-mozzarelle-helsinki#1.3', u'/biz/sis-deli-ja-cafe-helsinki-3#1.3', u'/biz/sandro-helsinki-2#1.6', u'/biz/hima-ja-sali-helsinki-3#2.4', u'/biz/dylan-helsinki-10#4.9']
#hrefs_to_resturants = [u'/biz/sis-deli-ja-cafe-helsinki-2#0.5-17', u'/biz/la-torrefazione-helsinki#0.4-38', u'/biz/karl-fazer-caf%C3%A9-helsinki-2#0.5-87', u'/biz/factory-helsinki-5#0.4-11', u'/biz/fleuriste-helsinki#0.8-20', u'/biz/caf%C3%A9-engel-helsinki-2#0.6-29', u'/biz/caf%C3%A9-daja-helsinki#0.9-10', u'/biz/bakers-helsinki#0.4-16', u'/biz/deli-cafe-maya-helsinki#1.2-11', u'/biz/ursula-helsinki#2.1-28', u'/biz/tin-tin-tango-helsinki#1.2-28', u'/biz/cargo-helsinki-2#1.4-7', u'/biz/piritta-helsinki#1.0-17', u'/biz/birgitta-helsinki#2.1-19', u'/biz/ipi-kulmakuppila-helsinki#1.4-6', u'/biz/moko-market-helsinki#1.5-21', u'/biz/cardemumma-helsinki-2#1.7-17', u'/biz/siltanen-helsinki#1.7-17', u'/biz/mille-mozzarelle-helsinki#1.3-6', u'/biz/sis-deli-ja-cafe-helsinki-3#1.3-5', u'/biz/sandro-helsinki-2#1.6-12', u'/biz/hima-ja-sali-helsinki-3#2.4-9', u'/biz/dylan-helsinki-10#4.9-13']

##
# Check each of the viable restaurants
##
viable_resturants = []
for href in hrefs_to_resturants:
    print 'Testing ' +href
    tmpArray = href[href.index("#")+1:].split("-")
    distance = float(tmpArray[0])
    review_count = int(tmpArray[1])
    # print distance
    # print review_count
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
                break

    if not open_weekend:
        print "Not open on weekends"
        continue
    print "Open on weekends"

    #Get Rating
    element = root_restaurant_soup.find("div", {"class": "rating-very-large"})
    tmpArray = element.get('class')[1].split("-") # gets, eg. i-stars--large-4-half and splits on '-'
    rating = float(tmpArray[4])
    if len(tmpArray)>5: # if there is a "-half"
        rating += 0.5
    print rating

    restaurant_name = root_restaurant_soup.find("h1", {"class": "biz-page-title"}).text.strip()

    #Get prices
    element = root_restaurant_soup.find("span", {"class": "price-range"})
    pricing = element.text.strip()
    viable_resturants.append((restaurant_name,href,rating,review_count,distance,pricing))
    time.sleep(1) # Trying to avoid getting blocked by Yelp
print viable_resturants

#viable_resturants = [(u'\n            SIS. Deli & Cafe\n        ', u'/biz/sis-deli-ja-cafe-helsinki-2#0.5-17', 4.5, 17, 0.5, u'\u20ac\u20ac'), (u'\n            La Torrefazione\n        ', u'/biz/la-torrefazione-helsinki#0.4-38', 4.0, 38, 0.4, u'\u20ac\u20ac'), (u'\n            Karl Fazer Caf\xe9\n        ', u'/biz/karl-fazer-caf%C3%A9-helsinki-2#0.5-87', 4.0, 87, 0.5, u'\u20ac\u20ac'), (u'\n            Factory\n        ', u'/biz/factory-helsinki-5#0.4-11', 3.5, 11, 0.4, u'\u20ac'), (u'\n            Fleuriste\n        ', u'/biz/fleuriste-helsinki#0.8-20', 4.5, 20, 0.8, u'\u20ac\u20ac'), (u'\n            Caf\xe9 Engel\n        ', u'/biz/caf%C3%A9-engel-helsinki-2#0.6-29', 4.0, 29, 0.6, u'\u20ac\u20ac'), (u'\n            Caf\xe9 DaJa\n        ', u'/biz/caf%C3%A9-daja-helsinki#0.9-10', 4.5, 10, 0.9, u'\u20ac\u20ac'), (u'\n            Baker\u2019s\n        ', u'/biz/bakers-helsinki#0.4-16', 3.5, 16, 0.4, u'\u20ac\u20ac'), (u'\n            Deli Cafe Maya\n        ', u'/biz/deli-cafe-maya-helsinki#1.2-11', 4.0, 11, 1.2, u'\u20ac'), (u'\n            Ursula\n        ', u'/biz/ursula-helsinki#2.1-28', 4.0, 28, 2.1, u'\u20ac\u20ac'), (u'\n            Tin Tin Tango\n        ', u'/biz/tin-tin-tango-helsinki#1.2-28', 4.0, 28, 1.2, u'\u20ac\u20ac'), (u'\n            Piritta\n        ', u'/biz/piritta-helsinki#1.0-17', 4.0, 17, 1.0, u'\u20ac\u20ac'), (u'\n            Birgitta\n        ', u'/biz/birgitta-helsinki#2.1-19', 4.0, 19, 2.1, u'\u20ac\u20ac'), (u'\n            IPI Kulmakuppila\n        ', u'/biz/ipi-kulmakuppila-helsinki#1.4-6', 3.5, 6, 1.4, u'\u20ac\u20ac'), (u'\n            Moko Market\n        ', u'/biz/moko-market-helsinki#1.5-21', 3.5, 21, 1.5, u'\u20ac\u20ac'), (u'\n            Cardemumma\n        ', u'/biz/cardemumma-helsinki-2#1.7-17', 3.5, 17, 1.7, u'\u20ac\u20ac'), (u'\n            Siltanen\n        ', u'/biz/siltanen-helsinki#1.7-17', 3.5, 17, 1.7, u'\u20ac\u20ac'), (u'\n            Mille Mozzarelle\n        ', u'/biz/mille-mozzarelle-helsinki#1.3-6', 3.5, 6, 1.3, u'\u20ac\u20ac'), (u'\n            SIS. Deli & Cafe\n        ', u'/biz/sis-deli-ja-cafe-helsinki-3#1.3-5', 4.0, 5, 1.3, u'\u20ac\u20ac'), (u'\n            Sandro\n        ', u'/biz/sandro-helsinki-2#1.6-12', 4.0, 12, 1.6, u'\u20ac\u20ac'), (u'\n            Ravintola Hima & Sali Kaapelitehdas\n        ', u'/biz/hima-ja-sali-helsinki-3#2.4-9', 4.0, 9, 2.4, u'\u20ac'), (u'\n            Dylan\n        ', u'/biz/dylan-helsinki-10#4.9-13', 4.0, 13, 4.9, u'\u20ac\u20ac')]

relative_scores = []
for restaurant in viable_resturants:
    #print "**********"
    rating_score = restaurant[2]
    #print rating_score
    review_count_score = restaurant[3]/100.0
    #print review_count_score
    distance_score = 3-restaurant[4]
    #print distance_score
    pricing_score = 2-len(restaurant[5])
    #print pricing_score

    #print restaurant[0].strip() + " " + BASE_URL + restaurant[1]
    total_score = rating_score + review_count_score + distance_score + pricing_score
    #print total_score
    relative_scores.append((restaurant,total_score))

#print relative_scores
relative_scores = sorted(relative_scores, key=lambda tup: tup[1], reverse=True)
#print relative_scores

print "**********"
print "*** TOP 5 Resturants"
print "**********"
print "(close to Kaivokatu 1, Helsinki)"
print

restaurant_labels=[]
distances=[]
ratings=[]
review_counts=[]
pricing_groups=[]
total_scores=[]

for i in range(5):
    restaurant = relative_scores[i][0]
    restaurant_name = restaurant[0].strip()
    restaurant_labels.append(restaurant_name)
    total_score = relative_scores[i][1]
    print "**********"
    print "*  Nr." + str((i+1)) +"  *"
    print "**********"
    print restaurant_name + " " + BASE_URL + restaurant[1][:restaurant[1].index("#")]  # [:restaurant[1].index("#")]
    # rating_score = restaurant[2]
    ratings.append(restaurant[2])
    # review_count_score = restaurant[3] / 100.0
    review_counts.append(restaurant[3])
    # distance_score = 3 - restaurant[4]
    distances.append(restaurant[4])
    # pricing_score = 2 - len(restaurant[5])
    pricing_groups.append(len(restaurant[5]))
    total_scores.append(total_score)
    print total_score

# Show as Graphs
matplotlib.rc('xtick', labelsize=8)
x = np.arange(len(restaurant_labels))

plt.bar(x, distances)
plt.xticks(x, restaurant_labels)
plt.ylabel("Distance (lower is better)")
plt.show()

plt.bar(x, ratings)
plt.xticks(x, restaurant_labels)
plt.ylabel("Rating")
plt.show()

plt.bar(x, review_counts)
plt.xticks(x, restaurant_labels)
plt.ylabel("Review Count")
plt.show()

plt.bar(x, pricing_groups)
plt.xticks(x, restaurant_labels)
plt.ylabel("Pricing Group (lower is better)")
plt.show()

plt.bar(x, total_scores)
plt.xticks(x, restaurant_labels)
plt.ylabel("Total Score")
plt.show()
