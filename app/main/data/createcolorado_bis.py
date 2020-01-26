import pandas as pd
from brewasisdb import add_colorado_bis

colorado_bis = pd.read_excel('cannabis_bis_colorado.xlsx', index_col=None, header=0)

colorado_bis.columns=['bus_file_num', 'lic_type', 'entity_name', 'trade_name', 'status', 'exp_data', 'facility_street', 'pre_direction', 'street_name', 'street_type', 'unit', 'city', 'zip_code']
print(colorado_bis.shape)
colorado_bis.drop_duplicates(subset ="bus_file_num", keep = 'first', inplace = True)
print(colorado_bis.shape)
colorado_bis.fillna(' ', inplace=True)
colorado_bis['adress'] = colorado_bis['facility_street'].astype(str) + ' ' + colorado_bis['pre_direction'].astype(str) + ' ' + colorado_bis['street_name'].astype(str) + ' ' + colorado_bis['street_type'].astype(str) + ' ' + colorado_bis['unit'].astype(str)
#colorado_bis['zip_code'] = colorado_bis['zip_code'].astype(int)
colorado_bis = colorado_bis.drop(colorado_bis.columns[[6, 7, 8, 9, 10]], axis=1)
#print(colorado_bis.loc[: , "zip_code"])


for index, row in colorado_bis.iterrows():
    add_colorado_bis(row['bus_file_num'], row['lic_type'], row['entity_name'], row['trade_name'], row['status'], row['exp_data'], row['adress'], row['city'], row['zip_code'])
