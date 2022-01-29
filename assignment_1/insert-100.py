from sqlalchemy import create_engine, text, Table, Column, MetaData
from sqlalchemy import Integer, Float, String, DateTime, BOOLEAN
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import insert
import pandas as pd
import numpy as np

'''Due to the size of the data being used, it is prudent to 
remove variables as soon they are no more needed. Thus, I
import the manual garbage collection library
'''
import gc


def insert_data(frame, chunksize=None):
  '''Helper function for converting `NaN` and `NaT` values in a
  pandas dataframe into compatible `NULL` types for sql.

  @param frame: the dataframe to parse
  @param chunksize: the chunk of the dataframe to parse starting from
    the first one. If `None`, all the records in the dataframe are parsed.
  
  @returns: a list of dictionary objects where each dict is a name-value 
    pair of the columns and corresponding values for each row in the dataframe
  '''
  column_names = list(map(str, frame.columns))
  ncols = len(column_names)
  data_list = [None] * ncols

  for i, (_, ser) in enumerate(frame.items()):
    vals = ser._values
    if vals.dtype.kind == "M":
      d = vals.to_pydatetime()
    elif vals.dtype.kind == "m":
      # store as integers, see GH#6921, GH#7076
      d = vals.view("i8").astype(object)
    else:
      d = vals.astype(object)

    assert isinstance(d, np.ndarray), type(d)

    if ser._can_hold_na:
      # Note: this will miss timedeltas since they are converted to int
      mask = pd.isna(d)
      d[mask] = None

    # error: No overload variant of "__setitem__" of "list" matches
    # argument types "int", "ndarray"
    data_list[i] = d  # type: ignore[call-overload]

  if chunksize is None:
    chunksize = frame.shape[0]

  chunk_iter = list(zip(*(arr[0:chunksize] for arr in data_list)))
  data = [dict(zip(column_names, row)) for row in chunk_iter]
  return data


# define database credentials
user = 'user' # replace with actual db user
password = 'password' # replace with db pass
host = 'localhost' # change to db host
port = 3306 # change to host port
db = 'population_db2' # name of schema

# setup database engine and session manager
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}')
Session = sessionmaker(engine)

# specify insert chunk size which is 100 per instruction
chunksize = 100

# read data from clean.csv
data = pd.read_csv('clean.csv')
data.SiteID = data.SiteID.astype('int64')

readings = data.drop(['Location', 'geo_point_2d'], axis=1)
# cast timestamps to datatypes compatible with the database
readings['Date Time'] = readings['Date Time'].astype('datetime64')
readings.DateEnd = readings.DateEnd.astype('datetime64')
readings.DateStart = readings.DateStart.astype('datetime64')

# remove unwanted data from memory
del data
gc.collect()

# set up ORM reference for readings table
meta = MetaData(bind=engine, schema=db)
readings_table = Table('readings', meta,
  Column('datetime', DateTime),
  Column('nox', Float),
  Column('no2', Float),
  Column('no', Float),
  Column('stationid-fk', Integer),
  Column('pm10', Float),
  Column('nvpm10', Float),
  Column('vpm10', Float),
  Column('nvpm2.5', Float),
  Column('pm2.5', Float),
  Column('vpm2.5', Float),
  Column('co', Float),
  Column('o3', Float),
  Column('so2', Float),
  Column('temperature', Float),
  Column('rh', Float),
  Column('airpressure', Float),
  Column('datestart', DateTime),
  Column('dateend', DateTime),
  Column('current', BOOLEAN),
  Column('instrumenttype', String)
)


# build orm statement
r_values = insert_data(readings, chunksize=chunksize)
stmnt = insert(readings_table).values(r_values)

# generate raw mysql statement
with engine.connect() as session:
  cursor = session.connection.cursor()
  compiled = stmnt.compile()

  raw_stmnt = cursor.mogrify(str(compiled), compiled.params)

# generate insert-100.sql file
with open('insert-100.sql', 'w') as f:
  f.write(raw_stmnt)