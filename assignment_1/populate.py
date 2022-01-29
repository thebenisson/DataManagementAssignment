from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Due to the size of the data being used, it is prudent to 
# remove variables as soon they are no more needed. Thus, I
# import the manual garbage collection library
import gc


# define database credentials
user = 'nino' # replace with actual db user
password = 'nino' # replace with db pass
host = 'localhost' # change to db host
port = 3306 # change to host port
db = 'population_db2' # name of schema


# setup database engine and session manager
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}')
Session = sessionmaker(engine)

# create database
with Session.begin() as session:
  session.execute(text(f'DROP SCHEMA IF EXISTS {db}'))
  session.execute(text(f'CREATE SCHEMA IF NOT EXISTS {db}'))

  # create stations table
  session.execute(text(f'DROP TABLE IF EXISTS `{db}`.`stations` ;'))
  session.execute(text(
    f'CREATE TABLE IF NOT EXISTS `{db}`.`stations` (\
      `stationid` INT NOT NULL,\
      `location` VARCHAR(48) NOT NULL,\
      `geo_point_2d` VARCHAR(48) NOT NULL,\
    PRIMARY KEY (`stationid`))\
    ENGINE = InnoDB;'
  ))
  
  # create readings table
  session.execute(text(f'DROP TABLE IF EXISTS `{db}`.`readings`;'))
  session.execute(text(
    f'CREATE TABLE IF NOT EXISTS `{db}`.`readings` (\
      `readingid` INT NOT NULL AUTO_INCREMENT,\
      `datetime` DATETIME NULL,\
      `nox` FLOAT NULL,\
      `no2` FLOAT NULL,\
      `no` FLOAT NULL,\
      `pm10` FLOAT NULL,\
      `nvpm10` FLOAT NULL,\
      `vpm10` FLOAT NULL,\
      `nvpm2.5` FLOAT NULL,\
      `pm2.5` FLOAT NULL,\
      `vpm2.5` FLOAT NULL,\
      `co` FLOAT NULL,\
      `o3` FLOAT NULL,\
      `so2` FLOAT NULL,\
      `temperature` FLOAT NULL,\
      `rh` FLOAT NULL,\
      `airpressure` FLOAT NULL,\
      `datestart` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,\
      `dateend` DATETIME NULL,\
      `current` VARCHAR(5) NOT NULL,\
      `stationid-fk` INT NOT NULL,\
      `instrumenttype` VARCHAR(32) NULL,\
    PRIMARY KEY (`readingid`),\
    CONSTRAINT `stationid`\
      FOREIGN KEY (`stationid-fk`)\
      REFERENCES `{db}`.`stations` (`stationid`)\
      ON DELETE CASCADE\
      ON UPDATE CASCADE)\
    ENGINE = InnoDB;'
  ))

  # create schema table
  session.execute(text(f'DROP TABLE IF EXISTS `{db}`.`schema`;'))
  session.execute(text(
    f'CREATE TABLE IF NOT EXISTS `{db}`.`schema` (\
      `measure` VARCHAR(16) NOT NULL,\
      `description` VARCHAR(70) NOT NULL,\
      `unit` VARCHAR(24) NOT NULL,\
    PRIMARY KEY (`measure`) )\
    ENGINE = InnoDB;'
  ))


# read data from clean.csv
data = pd.read_csv('/home/benisson/Workspace/UWEDMASS/assignment_1/clean.csv')
data.SiteID = data.SiteID.astype('int64')

# filter station data 
stations = data.filter(items=['SiteID', 'Location', 'geo_point_2d']).drop_duplicates(subset='SiteID')
# format column names
stations.columns = [column.lower().replace('siteid', 'stationid') for column in stations.columns]
print('\ninserting data into stations table...')
try:
  # create and populate stations table
  stations.to_sql('stations', con=engine, if_exists='append', index=False, schema=db)
  print('Stations data inserted')
except:
  print("Couldn't insert data into stations table.")
finally:
  del stations
  gc.collect()


# filter readings from data
readings = data.drop(['Location', 'geo_point_2d'], axis=1)
# cast timestamps to datatypes compatible with the database
readings['Date Time'] = readings['Date Time'].astype('datetime64')
readings.DateEnd = readings.DateEnd.astype('datetime64')
readings.DateStart = readings.DateStart.astype('datetime64')
# cast current column to string type
readings.Current = readings.Current.astype('string')
# format column names
readings.columns = [column.lower().replace(' ', '').replace('siteid', 'stationid-fk') for column in readings.columns]

print('\ninserting data into readings table...')
try:
  # create and insert data into readings table
  readings.to_sql('readings', if_exists='append', con=engine, chunksize=1000, index=False, schema=db)
  print('readings data inserted')
except:
  print("Couldn't insert data into readings table.")
finally:
  del readings, data
  gc.collect()

# create dataframe of data for the schema table
schema = pd.DataFrame({
  'measure': ['Date Time', 'NOx', 'NO2', 'NO', 'SiteID', 'PM10', 'NVPM10', 'VPM10', 'NVPM2.5', 'PM2.5',
    'VPM2.5', 'CO', 'O3', 'SO2', 'Temperature', 'RH', 'Air Pressure', 'Location', 'geo_point_2d',
    'DateStart', 'DateEnd', 'Current', 'Instrument Type'
  ],
  'description': [
    'Date and Time of measurement',
    'Concentration of oxides of nitrogen',
    'Concentration of nitrogen dioxide',
    'Concentration of nitric oxide',
    'Site ID for the station',
    'Concentration of particulate matter < 10 micron diameter',
    'Concentration of non-volatile particulate matter < 10 micron diameter',
    'Concentration of volatile particulate matter < 10 micron diameter',
    'Concentration of non-volatile particulate matter < 2.5 micron diameter',
    'Concentration of particulate matter < 2.5 micron diameter',
    'Concentration of volatile particulate matter < 2.5 micron diameter',
    'Concentration of carbon monoxide',
    'Concentration of ozone',
    'Concentration of sulphur dioxide',
    'Air Temprature',
    'Relative humidity',
    'Air pressure',
    'Text description of location',
    'Latitude and longitude',
    'The date monitoring started',
    'The date monitoring ended',
    'Is the monitor currently operating',
    'Classificationo of the instrument'
  ],
  'unit': ['datetime', 'ug/m3', 'ug/m3', 'ug/m3', 'integer', 'ug/m3', 'ug/m3', 'ug/m3',
    'ug/m3', 'ug/m3', 'ug/m3', 'mg/m3', 'ug/m3', 'ug/m3', 'oC', '%', 'mbar', 'text',
    'geo point', 'datetime', 'datetime', 'text', 'text'
  ]
})

print('\ninserting data into schema table...')
try:
  # create and insert data into schema table
  schema.to_sql('schema', if_exists='append', con=engine, chunksize=1000, index=False, schema=db)
  print('schema data inserted')
except Exception as err:
  print(f"Couldn't insert data into schema table. \n {err}")
finally:
  del schema
  gc.collect()
