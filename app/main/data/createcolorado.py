import pandas as pd
from brewasisdb import add_colorado

colorado = pd.read_excel('colorado_sales.xlsx', index_col=None, header=0)
print (colorado.head())
colorado.columns=['id', 'year', 'category', 'state', 'code', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']


for index, row in colorado.iterrows():
    add_colorado(row['id'], row['year'], row['category'], row['state'], row['code'], row['january'], row['february'], row['march'], row['april'], row['may'], row['june'], row['july'], row['august'], row['september'], row['october'], row['november'], row['december'])
