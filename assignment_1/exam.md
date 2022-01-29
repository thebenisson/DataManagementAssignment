# Assumed DB Model

| students | modules | course |
| --- | --- | --- |
| s_id | m_id | s_id |
| s_name | m_name | m_id |
| | m_credit | |

<em><strong style="text-decoration: underline">NB:</strong> Each colum represents an entity on the er diagram.</em>

# Pseudocode
```
This programs creates and populates a mysql database according to the ER diagram in 4a.
import: sqlalchemy
        pandas

engine = create sqlachemy engine using mysql connection url
session = create a db session manager using the engine

with session started:
  drop schema if it exists in the database
  create a new schema
  create students table
  create modules table
  create the course association table
close session

data = read csv into pandas dataframe
rename columns in the dataframe after those specified in the schema

students = filter student id and name columns in data into a new dataframe named after the students table

modules = filter module id, name and credit columns in data into a dataframe for the modules table

course = filter module id and student id columns in data into another dataframe for the association table

filtered_dataframes = create a dictionary of the filtered dataframes with their names as keys.

for dataframe in filtered_dataframes:
  try:
    call to_sql on the dataframe specifying engine, schema, table and isertion chunk (if necessary)
  except:
    output error message
end for


```
