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
sns.set_context("talk")
sns.set_style("white")

# pass in column names for each CSV
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']

users = pd.read_csv(
    'http://files.grouplens.org/datasets/movielens/ml-100k/u.user',
    sep='|', names=u_cols)

print(users.head())


# coding=utf-8
## all imports
import numpy as np
import urllib2
import bs4 #this is beautiful soup
import time
import matplotlib
import matplotlib.pyplot as plt
BASE_URL = 'https://www.yelp.se'
ORIGINAL_URL = BASE_URL +'/search?find_loc=Kaivokatu+1,+helsinki&start=0&cflt=breakfast_brunch&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2'
source = urllib2.urlopen(ORIGINAL_URL).read()
root_search_soup = bs4.BeautifulSoup(source,'html.parser')
TOTAL_RESULTS_PER_PAGE = 30
##
#Get result count
##
total_results_contents = root_search_soup.find("span",{"class":
"pagination-results-window"}).contents[0]
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
 search_result_divs = root_search_soup.findAll("div", {"class": "search-result"})
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
 hrefs_to_resturants.append(restaurant_a.get('href') + "#" + str(distance) + "-" +
str(review_count)) #Fastest way to just add the distance to the url
 print 'Handled ' + str(results_handled_count) + ' results on page ' + str(i+1)
print 'Got a total of ' + str(len(hrefs_to_resturants)) + ' viable results'
print hrefs_to_resturants
##
# Check each of the viable restaurants
##
viable_resturants = []
for href in hrefs_to_resturants:
 print 'Testing ' +href
 tmpArray = href[href.index("#")+1:].split("-")
 distance = float(tmpArray[0])
 review_count = int(tmpArray[1])
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
 if u"lör" in trow.findChild("th").text or u"sön" in trow.findChild("th").text:
 if len(trow.findChild("td").findChildren("span"))>0:
 open_weekend = True
 break
 if not open_weekend:
 print "Not open on weekends"
 continue
 print "Open on weekends"
 #Get Rating
 element = root_restaurant_soup.find("div", {"class": "rating-very-large"})
 tmpArray = element.get('class')[1].split("-") # gets, eg. i-stars--large-4-half and
splits on '-'
 rating = float(tmpArray[4])
 if len(tmpArray)>5: # if there is a "-half"
 rating += 0.5
 print rating
 restaurant_name = root_restaurant_soup.find("h1", {"class":
"biz-page-title"}).text.strip()
 #Get prices
 element = root_restaurant_soup.find("span", {"class": "price-range"})
 pricing = element.text.strip()
 viable_resturants.append((restaurant_name,href,rating,review_count,distance,pricing))
 time.sleep(1) # Trying to avoid getting blocked by Yelp
print viable_resturants
relative_scores = []
for restaurant in viable_resturants:
 rating_score = restaurant[2]
 review_count_score = restaurant[3]/100.0
 distance_score = 3-restaurant[4]
 pricing_score = 2-len(restaurant[5])
 total_score = rating_score + review_count_score + distance_score + pricing_score
 relative_scores.append((restaurant,total_score))
relative_scores = sorted(relative_scores, key=lambda tup: tup[1], reverse=True)
print "**********"
print "*** TOP 5 Restaurants"
print "**********"
print "(close to Kaivokatu 1, Helsinki)"
print
restaurant_labels=[]
distances=[]
ratings=[]
review_counts=[]
pricing_groups=[]
total_scores=[]
# Calculate and Print Score for Top 5
for i in range(5):
 restaurant = relative_scores[i][0]
 restaurant_name = restaurant[0].strip()
 restaurant_labels.append(restaurant_name)
 total_score = relative_scores[i][1]
 print "**********"
 print "* Nr." + str((i+1)) +" *"
 print "**********"
 print restaurant_name + " " + BASE_URL + restaurant[1][:restaurant[1].index("#")]
 ratings.append(restaurant[2])
 review_counts.append(restaurant[3])
 distances.append(restaurant[4])
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