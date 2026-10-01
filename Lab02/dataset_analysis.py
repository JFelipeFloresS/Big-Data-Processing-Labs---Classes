# read Lab02/my_dataset_complete_31_files/siri.20130101.csv
import pandas as pd

df = pd.read_csv('my_dataset_complete_31_files/siri.20130101.csv')

# add column headers: date, bus_line, bus_line_pattern, congestion, longitude, latitude, delay, vehicle_id, closer_stop, at_stop_stop
df.columns = ['date', 'bus_line', 'bus_line_pattern', 'congestion', 'longitude', 'latitude', 'delay', 'vehicle_id', 'closer_stop', 'at_stop_stop']

# print the first 5 rows of the dataframe
print(df.head())

# print the column types of the dataframe
print(df.dtypes)

# list bus lines in the set
bus_lines = df['bus_line'].unique()
print("Bus lines in the dataset ({}):".format(len(bus_lines)))
for i, line in enumerate(bus_lines):
    print(line, end=', ' if i < len(bus_lines) - 1 else '\n')

print("Maximum delay in the dataset:", df['delay'].max())
print("Minimum delay in the dataset:", df['delay'].min())

# check top 10 most delayed bus lines
top_10_most_delayed_lines = df.groupby('bus_line')['delay'].mean().nlargest(10)
print("Top 10 most delayed bus lines:")
print(top_10_most_delayed_lines)

# check top 10 least delayed bus lines
top_10_least_delayed_lines = df.groupby('bus_line')['delay'].mean().nsmallest(10)
print("Top 10 least delayed bus lines:")
print(top_10_least_delayed_lines)