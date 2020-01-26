import pandas as pd
from brewasisdb import add_oregon_bis

oregon_bis = pd.read_excel('cannabis_bis_oregon.xlsx', index_col=None, header=0)

oregon_bis.columns=['lic_num', 'lic_name', 'bus_name', 'lic_type', 'active', 'county', 'retail', 'medical', 'hemp']
#print(oregon_bis.shape)
#oregon_bis.drop_duplicates(subset ="lic_num", keep = 'first', inplace = True)
#print(oregon_bis.shape)
oregon_bis.fillna(' ', inplace=True)
#colorado_bis['adress'] = colorado_bis['facility_street'].astype(str) + ' ' + colorado_bis['pre_direction'].astype(str) + ' ' + colorado_bis['street_name'].astype(str) + ' ' + colorado_bis['street_type'].astype(str) + ' ' + colorado_bis['unit'].astype(str)
#colorado_bis['zip_code'] = colorado_bis['zip_code'].astype(int)
#colorado_bis = colorado_bis.drop(colorado_bis.columns[[6, 7, 8, 9, 10]], axis=1)
#print(colorado_bis.loc[: , "zip_code"])


for index, row in oregon_bis.iterrows():
    add_oregon_bis(row['lic_num'], row['lic_name'], row['bus_name'], row['lic_type'], row['active'], row['county'], row['retail'], row['medical'], row['hemp'])
