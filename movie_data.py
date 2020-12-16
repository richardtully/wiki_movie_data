'''
This script scrapes wikipedia and collects a list of url's of wikipedia movie pages
The 'get_movie_info_function' is then called on each of these pages to extract relevant information
The info scraped is a dictionary of stats about the movie
This data can then be saved as wiki_movie_info.pickle
'''



import requests
from bs4 import BeautifulSoup
from get_movie_info_function import MovieInfoGetter #get_movie_info
import matplotlib.pyplot as plt
import pickle




mig = MovieInfoGetter()


def get_movie_list(url):
	'''
	INPUT: one of wikipedias standard 'wiki/19--_in_film' URL's
	OUTPUT: a list of URL's of the hightest grossing movies from that year
	'''
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	#2006 has an extra table 'This article needs additional citations for verification'
	if '2006' in url:
		movie_table = soup.find_all('table')[4]
	else:
		movie_table = soup.find_all('table')[3]
	movie_row = movie_table.find_all('tr')
	movie_list = []
	for thing in movie_row:
		movie_list.append(str(thing.find('td')))
	del movie_list[0]
	movie_list2 = []
	for text in movie_list:
		x = text.split('"')
		x = [i for i in x if '/wiki/' in i]
		movie_list2.append('https://en.wikipedia.org' + x[0])
	return movie_list2


# Build a list of url's (using get_movie_list) to feed into the movie info getter
big_list =[]
for year in range(1988,2020):
	print(year)
	url = 'https://en.wikipedia.org/wiki/' + str(year) + '_in_film'
	big_list += get_movie_list(url)


# Build a list of dictionaries of info about each movie corrosponding to a url from big_list
movie_data_list=[]
for url in big_list:
	movie_data_list.append(mig.get_movie_info(url))



# This let's us save (pickle) the info we find. Be careful, it will overwrite our old file!
# with open('wiki_movie_info.pickle','wb') as handle:
# 	pickle.dump(movie_data_list, handle, protocol=pickle.HIGHEST_PROTOCOL)



