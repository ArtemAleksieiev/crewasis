import pandas as pd
from brewasisdb import add_population

population = pd.read_excel('population.xlsx', index_col=None, header=0)
population.columns=['state', 'pop', 'percent', 'adults']
population['percent'] = population['percent'].apply(lambda x: round(x, 4))

for index, row in population.iterrows():
    add_population(row['state'], row['pop'], row['percent'], row['adults'])
