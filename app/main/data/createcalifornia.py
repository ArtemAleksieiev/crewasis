import pandas as pd
from brewasisdb import add_california

california = pd.read_excel('cannabis_bis.xlsx', index_col=None, header=0)

california.columns=['lic_num', 'lic_type', 'owner', 'contact', 'e-mail', 'phone', 'website', 'structure', 'adress', 'status', 'issue', 'expiration', 'activities', 'use']
print(california.head())


for index, row in california.iterrows():
    add_california(row['lic_num'], row['lic_type'], row['owner'], row['contact'], row['e-mail'], row['phone'], row['website'], row['structure'], row['adress'], row['status'], row['issue'], row['expiration'], row['activities'], row['use'])
