# Task 5 - NoSQL Data Model

## Database
MongoDB was used in this project.

## Data Model
I maintained a flat structure for the data given its size and the fact that redundancy boosts retrieval efficiency with NoSQL databases. The data is stored under a records collection in a database named pollution

## Implementation & Data Import
```python
# importing required libraries
from pymongo import MongoClient
import pandas as pd.
import gc

# setting up pollution db and its connection client to 
# mongo server running on localhost and port 27017
client = MongoClient('localhost', '27017')
db = client.pollution

# importing data into a pandas dataframe
data = pd.read_csv('clean.csv')
# force SiteIDs to be integers
data.SiteID = data.SiteID.astype('int64')
# cast timestamps to datatypes compatible with the database
data['Date Time'] = data['Date Time'].astype('datetime64')
data.DateEnd = data.DateEnd.astype('datetime64')
data.DateStart = data.DateStart.astype('datetime64')

# restructure geopoints for easy use 
# (convert the string into an array)
data.geo_point_2d = data.geo_point_2d.str.split(',')

# convert dataframe to array of key-value pairs of entries
records = data.to_dict(orient='records')

# inserting the data into the database (records collection)
db.collection.records.insertmany(records)

# manually clean memory
del data, records
gc.collect()
```

## Query
The queries shown below was used to implement the NoSQL version of query c in Task 4.

```python
results = records.aggregate([
  {
    '$match': {
      "Date Time": {
        "$gte": datetime.strptime('01-01-19', '%d-%m-%y'),
        "$lte": datetime.strptime('31-12-19', '%d-%m-%y')
      }
    }
  },
  {
    "$group": {
      "_id": "$SiteID",
      "Location": {"$first": "$Location"},
      "MeanPM2_5": {"$avg": "$PM2.5"},
      "MeanVPM2_5": {"$avg": "$VPM2.5"}
    }
  }
])
```