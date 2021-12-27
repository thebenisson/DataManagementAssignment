import pandas as pd
import numpy as np

print("Remove all dud records where there is no value for SiteID or there is mismatch between SiteID and Location")

df = pd.read_csv('cropped.csv')
# define station parameters
stations = {
  188 : 'AURN Bristol Center',
  203 : 'Brislington Depot',
  206 : 'Rupert Street',
  209 : 'IKEA M32',
  213 : 'Old Market',
  215 : 'Parson Street School',
  228 : 'Temple Meads Station',
  270 : 'Wells Road',
  271 : 'Trailer Portway P&R',
  375 : 'Newfoundland Road Police Station',
  395 : "Shiner's Garage",
  452 : 'AURN St Pauls',
  447 : 'Bath Road',
  459 : 'Cheltenham Road \\ Station Road',
  463 : 'Fishponds Road',
  481 : 'CREATE Centre Roof',
  500 : 'Temple Way',
  501 : 'Colston Avenue'
}

# print out entries without SiteIDs of no Locations for specified SiteIDs
print('entries without SiteIDs of no Locations for specified SiteIDs')
print(df[df.SiteID.isnull() | ~df.SiteID.isin(stations.keys())].filter(items=['SiteID', 'Location']))

# filter null SiteIDs and siteIDs not in stations
df = df[df.SiteID.notnull() & df.SiteID.isin(stations.keys())]

# gather 'index' on all entries where siteID doesn't match location
indices = [ index for index, SiteID, Location in np.array(df[['Date Time', 'SiteID', 'Location']]) if stations[SiteID]==Location ]

# print out site mismatches
print('SiteID and Location mismatches')
print(df[~df['Date Time'].isin(indices)].filter(items=['SiteID', 'Location']))

# filter entries whose indices are in the collected 'Date Time' indices
df = df[df['Date Time'].isin(indices)]

# save to clean.csv
df.to_csv('clean.csv', index=False)
print("Data saved as 'clean.csv'")