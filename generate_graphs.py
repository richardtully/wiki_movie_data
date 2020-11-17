import matplotlib.pyplot as plt
import pickle

infile = open('wiki_movie_info.pickle','rb')
wiki_movie_info = pickle.load(infile)
infile.close()


# Here are the 5 different data points taken from each film (That you can make a graph with):
# 'Budget'
# 'Box office'
# 'Profit'
# 'Running time' 
# 'Plot length'
# Choose two of the above labels and set the variables x_axis and y_axis to them.

x_axis = 'Budget'
y_axis = 'Profit'

plt.scatter([i[x_axis] for i in wiki_movie_info], [i[y_axis] for i in wiki_movie_info], marker = '.')
plt.xlabel(x_axis)
plt.ylabel(y_axis)
plt.suptitle('Data from top 10 highest grossing films per year since 1988')


plt.show()
