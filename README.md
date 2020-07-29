# wiki_movie_data
Web sraping various data from wikipedia pages to make inferences about the highest earning movies of the last few decades.

This code uses BS4 to scrape Name, Budget, Box office, Profit, Running time and Plot length from the top 10 grossing movies from each year since 1988.

It uses fixer.io API to convert currencies of films whose budget and box office are not given in USD.

It saves the collected data in a dictionary using Pickle and then produces a graph from this dictionary. 
