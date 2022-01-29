#importing required libraries
import sqlalchemy
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import pymysql
import pandas as pd

'''Due to the size of the data being used, it is prudent to 
remove variables as soon they are no more needed
'''
import gc

# define database credentials
user = 'user' # replace with actual db user
password = 'password' # replace with db pass
host = 'localhost' # change to db host
port = 3306 # change to host port

# name of schema to be created and used by this script. Be careful no db exists on your 
# server with the same name, such will be dropped and a new on created.
# don't change it also as it will conflict with the name defined in the SQL script.
db = 'pollution'

# setup database engine and session manager
engine = sqlalchemy.create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}')
Session = sessionmaker(engine)

# create database from pollution.sql file
print('Executing commands in pollution.sql')
with open('pollution.sql', 'r') as sqlfile:
  query = ''
  # skip comments in file and execute full sql statements
  for line in sqlfile:
    if not line.startswith('--') and line.strip('\n'):
      query += line.strip('\n')

      if query.endswith(';'):
        try:
          with Session.begin() as session:
            session.execute(text(query))
        except:
            print(f"could not execute `{query}`. Check the query or the connection")
            raise Exception('SQL execution error')
        finally:
          query = ''

# read data from clean.csv for insertion into database
df = pd.read_csv('clean.csv')

# insert data into station table. This table contains data on monitoring sites
stations = df.filter(items=['SiteID', 'Location', 'geo_point_2d']).drop_duplicates(subset='SiteID')
stations.SiteID = stations.SiteID.astype('int64')
print('\ninserting data into stations table...')
try:
  stations.to_sql('stations', con=engine, if_exists='append', index=False, schema=db)
  print('Stations data inserted')
except:
  print("Couldn't insert data into stations table.")
finally:
  del stations
  gc.collect()

# filter out geolocation data
geopoints = df.filter(items=["SiteID", "geo_point_2d"]).drop_duplicates(subset='SiteID')
# cast site id into appropriate data type
geopoints.SiteID = geopoints.SiteID.astype('int64')
# format geopoints into latitudes and longitudes
geopoints[['latitude', 'longitude']] = geopoints.geo_point_2d.str.split(',', expand=True)
del geopoints['geo_point_2d']

print('\nInserting data into geopoints table...')
try:
  geopoints.to_sql('geopoints', con=engine, if_exists='append', index=False, schema=db)
  print('geopoints data inserted')
except:
  print("Couldn't insert data into geopoints table.")
finally:
  del geopoints
  gc.collect()

# filter out instrument types
instru_types = df.filter(items=['Instrument Type']).drop_duplicates()

print('\ninserting data into istruments table...')
try:
  instru_types.to_sql('instruments', con=engine, if_exists='append', index=False, schema=db)
  print('instruments data inserted')
except:
  print("Couldn't insert data into instruments table.")
finally:
  del instru_types
  gc.collect()

# insert data into records table
records = df.drop(['Location', 'geo_point_2d'], axis=1)
# cast timestamps to datatypes compatible with the database
records['Date Time'] = records['Date Time'].astype('datetime64')
records.DateEnd = records.DateEnd.astype('datetime64')
records.DateStart = records.DateStart.astype('datetime64')

print('\ninserting data into records table...')
try:
  records.to_sql('records', if_exists='append', con=engine, chunksize=1000, index=False, schema=db)
  print('records data inserted')
except:
  print("Couldn't insert data into records table.")
finally:
  del records, df
  gc.collect()