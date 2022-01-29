import pandas as pd
import numpy as np

print("Cropping DataSet: Removing entries older that 2010 Jan 01, 00:00")

df = pd.read_csv('bristol-air-quality-data.csv', sep=';')

# delete entries older than 2010-01-01 00:00
df = df[df['Date Time'].astype('datetime64') >= pd.Timestamp('2010-01-01T00')]
# df = df[~df.DateStart.isna()]

# save to new csv
df.to_csv('cropped.csv', index=False)
print("Data cropped. New dataset saved as cropped.csv")