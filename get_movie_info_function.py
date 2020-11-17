'''
This script creates a class with functions that are used in the main script (movie_data).
'''


import requests
from bs4 import BeautifulSoup
import re


# Fixer.io identifies currencies by a three letter code - wikipedia uses the currencies symbol
symbol_to_currency_code = {
'£': 'GBP',
'CN¥': 'CNY',
'JP¥':'JPY',
'¥': 'JPY',
'$':'USD'	
}


class MovieInfoGetter:
	'''
	This Class defines an object that scrapes info from a standard wikipedia movie page.
	This is the info that it scrapes: Name, Budget, Box office, Profit, Running time and Plot length
	'''
	def __init__(self):
		#  ccy_conversion_table is a JSON object obtained from fixer.io
		self.ccy_conversion_table =  requests.get('http://data.fixer.io/api/latest?access_key=22074ea7114b8e2d29fb24e25f15f99a').json()
		# symbol_to_currency_code is a dictionary that converts between currency symbols and fixer.io's 3 letter currency codes
		self.symbol_to_currency_code =  {
		'£': 'GBP',
		'CN¥': 'CNY',
		'JP¥':'JPY',
		'¥': 'JPY',
		'$':'USD'	
		}

	# Grab 6 peices of info from a wiki movie page
	def get_movie_info(self, url):
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')

		def find_plot_len(soup):
			plot_title = soup.find(id = 'Plot')
			if plot_title == None:
				plot_title =soup.find(id = 'Synopsis')
				 
			plot_text_start = plot_title.find_parent()
			plot = ''
			for sibling in plot_text_start.next_siblings:
				if sibling.name == 'p':
					plot += sibling.text
				elif sibling.name == 'h2':
					break
			return len(plot)

		def find_running_time(soup):
			running_time_label = soup.find(name = 'div', text = 'Running time')
			running_time_parent =  running_time_label.parent 
			running_time_text = running_time_parent.next_sibling.text
			running_time=''
			for i in list(running_time_text):
				if i in ['.','0','1','2','3','4','5','6','7','8','9']:
					running_time += i
				else:
					break
			return int(running_time)

		def convert_to_USD(input_currency, ammount):
			print('input_currency: ' + input_currency)
			print('ammount: ' + str(ammount))

			book = self.ccy_conversion_table
			if input_currency in self.symbol_to_currency_code:
				input_currency = self.symbol_to_currency_code[input_currency]
			ammount_in_USD = book['rates']['USD']/book['rates'][input_currency]*ammount
			print('amount in USD: ' + str(ammount_in_USD))
			return(ammount_in_USD)

		def find_budget(soup):
			budget_label = soup.find(name = 'th', text = 'Budget')
			budget_text = budget_label.next_sibling.text
			budget_text = budget_text.replace("\n",'')
			budget_text = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", budget_text)
			budget = ''
			currency = ''
			for i in list(budget_text):
				if i in ['.','0','1','2','3','4','5','6','7','8','9']:
					budget += i
				elif budget != '':
					break
				else:
					currency += i
			budget = float(budget)
			if 'million' in budget_text:
				budget *= 1000000
			if currency != '$':
				budget = convert_to_USD(currency, budget)
			return budget 

		def find_box_office(soup):
			box_office_label = soup.find(name = 'th', text = 'Box office')
			box_office_text = box_office_label.next_sibling.text
			box_office_text = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", box_office_text)
			box_office = ''
			currency = ''
			for  i in list(box_office_text):
				if i in ['.','0','1','2','3','4','5','6','7','8','9']:
					box_office += i
				elif box_office != '':
					break
				else:
					currency += i
			box_office = float(box_office)
			if 'million' in box_office_text:
				box_office *= 1000000
			if 'billion' in box_office_text:
				box_office *= 1000000000
			if currency != '$':
				box_office = convert_to_USD(currency, box_office)
			return box_office  

		def find_profit(soup):
			x = find_budget(soup)
			y = find_box_office(soup)
			profit = y/x
			return profit



		movie_info = {
		'Name': url.split('/')[-1].replace('_',' '),
		'Budget': find_budget(soup),
		'Box office': find_box_office(soup),
		'Profit' : find_profit(soup),
		'Running time' : find_running_time(soup),
		'Plot length' : find_plot_len(soup)
		}
		return movie_info
