# begin processing phase here
import pandas as pd
import plotly.express as px
from plotly.offline import init_notebook_mode

init_notebook_mode(connected=True)
import plotly.io as pio

pio.renderers.default = "browser"

import matplotlib.pyplot as plt
import seaborn as sea

# to work with 12 CSV files separately is going to be difficult, so I will merge all of them into one big file to get
# a better view. Importing datasets from aug 2022 - jul 2023:
aug_2022 = pd.read_csv(
    "~/Documents/Data Analytics/Google-Data-Analytics-Capstone/Cyclistic_Files/CSV Files/2022_08-divvy-tripdata.csv")
sept_2022 = pd.read_csv(
    "~/Documents/Data Analytics/Google-Data-Analytics-Capstone/Cyclistic_Files/CSV Files/2022_09-divvy-tripdata.csv")
oct_2022 = pd.read_csv(
    "~/Documents/Data Analytics/Google-Data-Analytics-Capstone/Cyclistic_Files/CSV Files/2022_10-divvy-tripdata.csv")
nov_2022 = pd.read_csv(
    "~/Documents/Data Analytics/Google-Data-Analytics-Capstone/Cyclistic_Files/CSV Files/2022_11-divvy-tripdata.csv")
dec_2022 = pd.read_csv(
    "~/Documents/Data Analytics/Google-Data-Analytics-Capstone/Cyclistic_Files/CSV Files/2022_12-divvy-tripdata.csv")
jan_2023 = pd.read_csv(
    "~/Documents/Data Analytics/Google-Data-Analytics-Capstone/Cyclistic_Files/CSV Files/2023_01-divvy-tripdata.csv")
feb_2023 = pd.read_csv(
    "~/Documents/Data Analytics/Google-Data-Analytics-Capstone/Cyclistic_Files/CSV Files/2023_02-divvy-tripdata.csv")
mar_2023 = pd.read_csv(
    "~/Documents/Data Analytics/Google-Data-Analytics-Capstone/Cyclistic_Files/CSV Files/2023_03-divvy-tripdata.csv")
apr_2023 = pd.read_csv(
    "~/Documents/Data Analytics/Google-Data-Analytics-Capstone/Cyclistic_Files/CSV Files/2023_04-divvy-tripdata.csv")
may_2023 = pd.read_csv(
    "~/Documents/Data Analytics/Google-Data-Analytics-Capstone/Cyclistic_Files/CSV Files/2023_05-divvy-tripdata.csv")
jun_2023 = pd.read_csv(
    "~/Documents/Data Analytics/Google-Data-Analytics-Capstone/Cyclistic_Files/CSV Files/2023_06-divvy-tripdata.csv")
jul_2023 = pd.read_csv(
    "~/Documents/Data Analytics/Google-Data-Analytics-Capstone/Cyclistic_Files/CSV Files/2023_07-divvy-tripdata.csv")

# as all of the CSV files have the same column names, we will concatenate the 12 files from 2022 to 2023
final_file = pd.concat([aug_2022, sept_2022, oct_2022, nov_2022, dec_2022, jan_2023, feb_2023,
                        mar_2023, apr_2023, may_2023, jun_2023, jul_2023],
                       ignore_index=True)

# checking for null values
print(final_file.isna().sum())
# remove null values
final_file.dropna(inplace=True)

# delete columns that i won't be using for the analysis
final_file = final_file.drop(['start_station_id', 'end_station_id', 'end_station_name',
                              'start_lat', 'start_lng', 'end_lat', 'end_lng'], axis=1)

# convert started_at and ended_at columns to datetime datatype
final_file['started_at'] = final_file['started_at'].astype('datetime64[ns]')
final_file['ended_at'] = final_file['ended_at'].astype('datetime64[ns]')

# creating a new column called ride_length for the file
final_file['ride_length'] = (final_file['ended_at'] - final_file['started_at']) / pd.Timedelta(minutes=1)
final_file['ride_length'] = final_file['ride_length'].astype('int32')

final_file.sort_values(by='ride_length')

# check for negative numbers and remove them
final_file[final_file['ride_length'] < 0].count()

final_file = final_file[final_file['ride_length'] > 0]
final_file = final_file.reset_index()
final_file = final_file.drop(columns='index')

# get start day of the week, and split the start date into date, time, month, and year for easier analysis
final_file['start_date'] = final_file['started_at'].dt.day
final_file['start_time_hour'] = final_file['started_at'].dt.hour
final_file['start_day_of_week'] = final_file['started_at'].dt.day_name()
final_file['start_month'] = final_file['started_at'].dt.month_name()
final_file['start_year'] = final_file['started_at'].dt.year

# check number of unique values
final_file.nunique()

# check for duplicate values in the file
final_file['ride_id'].duplicated().sum()

# converting the latest processed file before we begin the analyse phase to CSV
final_file_clean = final_file
final_file_clean.to_csv(
    "~/Documents/Data Analytics/Google-Data-Analytics-Capstone/Cyclistic_Files/CSV Files/Cyclistic_Aug_2022_Jul_2023_clean.csv")

# begin analyse phase here
# order the above properly, since the days of the week are all over the place
days_of_the_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
final_file_clean['start_day_of_week'] = pd.Categorical(final_file_clean['start_day_of_week'],
                                                       categories=days_of_the_week_order, ordered=True)

# as the data begins from August 2022, we will order the months accordingly until July 2023
month_order = ['August', 'September', 'October', 'November', 'December', 'January', 'February', 'March', 'April', 'May',
               'June', 'July']
final_file_clean['start_month'] = pd.Categorical(final_file_clean['start_month'], categories=month_order, ordered=True)

# asking the most basic question - how many members/casual riders exist in the combined dataset?
percentage_users = round(final_file_clean['member_casual'].value_counts(normalize=True) * 100, 1)
print(percentage_users)

# here we see that the number of casual riders is far less than the number of members. Let us now see the type of bikes that were used
percentage_bikes = round(final_file_clean['rideable_type'].value_counts(normalize=True) * 100, 1)
print(percentage_bikes)

# avg ride length as seen per day of the week for both members and casual riders
avg_ride_length_per_user = final_file_clean.groupby(['member_casual', 'start_day_of_week']).ride_length.mean()
print(avg_ride_length_per_user)

# avg ride length as seen per hour for both types of users
print(final_file_clean.groupby(['member_casual', 'start_time_hour']).ride_length.mean())

# avg ride length as seen per months of the year for both members/casual riders
print(final_file_clean.groupby(['member_casual', 'start_month']).ride_length.mean())

# Top 5 busiest starting stations for both members and casual riders
n = 5
top_5_station_names = final_file_clean['start_station_name'].value_counts()[:n].index.to_list()
print(top_5_station_names)

# get the average riding length for each user from the list
final_file_clean_1 = final_file_clean.groupby('member_casual', as_index=False)['ride_length'].agg('mean')
print(final_file_clean_1)

# now we'll link the avg ride length to the days of the week, month, and hopefully time as well for the different users
final_file_clean_2 = final_file_clean.groupby(['member_casual', 'start_day_of_week'], as_index=False)[
    'ride_length'].agg('mean')
print(final_file_clean_2)

final_file_clean_3 = final_file_clean.groupby(['member_casual', 'start_month'], as_index=False)['ride_length'].agg(
    'mean')
print(final_file_clean_3)

final_file_clean_4 = final_file_clean.groupby(['member_casual', 'start_time_hour'], as_index=False)['ride_length'].agg(
    'mean')
print(final_file_clean_4)

# now we'll link the avg ride length to the types of bikes used by both casual riders and members
final_file_clean_5 = final_file_clean.groupby(['member_casual', 'rideable_type'], as_index=False)['ride_length'].agg(
    'mean')
print(final_file_clean_5)

# count the rides for both users and bike types
final_file_clean_6 = final_file_clean.groupby(['member_casual', 'rideable_type'])['ride_id'].count().rename_axis(
    ['member_casual', 'rideable_type']).reset_index(name='count')
print(final_file_clean_6)

# count the number of rides by each month for types of users
final_file_clean_7 = final_file_clean.groupby(['member_casual', 'start_month'], as_index=False)['ride_id'].agg('count')
print(final_file_clean_7)

# count the number of rides by the hour for types of users
final_file_clean_01 = final_file_clean.groupby(['member_casual', 'start_time_hour'], as_index=False)['ride_id'].agg(
    'count')
print(final_file_clean_01)

# count the number of rides for both users by day of the week
final_file_clean_8 = final_file_clean.groupby(['member_casual', 'start_day_of_week'], as_index=False)['ride_id'].agg(
    'count')
print(final_file_clean_8)

# the number of rides in the top 5 stations per user
final_file_clean_0 = final_file_clean.groupby(['member_casual', 'start_station_name'], as_index=False)['ride_id'].agg(
    'count')
final_file_clean_0 = final_file_clean_0.sort_values('ride_id', ascending=False)
print(final_file_clean_0)

# plotting pie charts for:
# 1. total percentage of users
# 2. total percentage of bikes used by the company
# 3. avg ride length of users
member_casual = ['Members', 'Casual Riders']
plt.figure(figsize=(10, 7))
plt.pie(percentage_users, labels=member_casual, autopct="%1.0f%%")
plt.title('Total Percentage of Users')
plt.show()

bike_types = ['Classic Bike', 'Docked Bike', 'Electric Bike']
plt.figure(figsize=(10, 7))
plt.pie(percentage_bikes, labels=bike_types, autopct="%1.1f%%")
plt.title('Total Percentage of Bikes Used by both Casual Rides and Members')
plt.show()

plt.figure(figsize=(10, 7))
plt.pie(final_file_clean_1['ride_length'], labels=final_file_clean_1['member_casual'], autopct="%1.1f%%")
plt.title("Average Riding Minutes per Rider from 2022-2023")
plt.savefig('Average Riding Minutes per Rider from 2022-2023', dpi=300, bbox_inches='tight')
plt.show()

# we will then plot the number of bikes (all types) used per user using various parameters as mentioned above
# 1. number of bikes used per user depending on type
# 2. count of bike rides per hour
# 3. count of bike rides per day
# 4. count of bike rides per month
final_file_clean_7 = final_file_clean.groupby(['rideable_type', 'member_casual'], as_index=False).count()

fig = px.bar(final_file_clean_7, x='rideable_type', y='ride_id',
             color='member_casual',
             barmode='group', text='ride_id',
             labels={'ride_id': 'No. of Rides', 'member_casual': 'Member/Casual Rider', 'rideable_type': 'Bike Type'},
             hover_name='member_casual', hover_data={'member_casual': False},
             color_discrete_map={'Casual Rider': '#9ACD32', 'Member': '#CD3700'},
             title='Preferred Bikes for Member vs Casual Rider')
fig.show()

fig = plt.figure(figsize=(10, 7))
sea.barplot(x='start_time_hour', y='ride_id', hue='member_casual', data=final_file_clean_01, legend=False)
plt.title('No. of Hourly Bike Rides - Members vs. Casual Riders')
plt.xlabel('Hours')
plt.ylabel('Count of Bike Rides')
plt.legend(title='Members/Casual Riders', labels=['Member', 'Casual Rider'])
plt.show()

fig = plt.figure(figsize=(10, 7))
sea.barplot(x='start_day_of_week', y='ride_id', hue='member_casual', data=final_file_clean_8, legend=False)
plt.title('No. of Daily Bike Rides in a Week - Members vs. Casual Riders')
plt.xlabel('Day of the Week')
plt.ylabel('Count of Bike Rides')
plt.legend(title='Members/Casual Riders', labels=['Member', 'Casual Rider'])
plt.show()

final_file_clean_7 = final_file_clean.groupby(['member_casual', 'start_month'], as_index=False)['ride_id'].agg('count')
fig = px.bar(final_file_clean_7, x='start_month', y='ride_id',
             color='member_casual', barmode='group',
             text='ride_id',
             labels={'ride_id': 'No. of Bike Rides', 'member_casual': 'Member/Casual Riders',
                     'start_month': 'Months (Aug 22 - Jul 23)'},
             hover_name='member_casual', hover_data={'member_casual': False},
             color_discrete_map={'casual': '#000080', 'member': '#FF6A6A'})
fig.show()

# now we will plot for the average ride lengths.
# 1. average ride length per user per day of the week
fig = plt.figure(figsize=(10, 7))
sea.barplot(x='start_day_of_week', y='ride_length', hue='member_casual', data=final_file_clean_2)
plt.title("Average ride length per Day: Members vs Casual Riders")
plt.xlabel("Day of the Week")
plt.ylabel("Avg Ride Length")
plt.show()

# 2. average ride length per user per month. Check to see if this frame has NA values
final_file_clean_3 = round(
    final_file_clean.groupby(['member_casual', 'start_month'], as_index=False)['ride_length'].agg('mean'), 2)
fig = px.bar(final_file_clean_3, x='start_month', y='ride_length',
             color='member_casual', barmode='group', text='ride_length',
             labels={'ride_length': 'Avg Ride Length (minutes)', 'member_casual': 'Member/Casual Riders',
                     'start_month': 'Month (Aug 2022 - Jul 2023)'},
             hover_name='member_casual', hover_data={'member_casual': False, 'ride_length': True},
             color_discrete_map={'casual': '#8B3A62', 'member': '#008B00'})
fig.show()

# 3. average hourly ride length per user
final_file_clean_4 = round(
    final_file_clean.groupby(['member_casual', 'start_time_hour'], as_index=False)['ride_length'].agg('mean'), 2
)
fig = px.bar(final_file_clean_4, x='start_time_hour', y='ride_length',
            color='member_casual', barmode='group', text='ride_length',
            labels={'ride_length': 'Avg Ride Length (in minutes)', 'member_casual': 'Members/Casual Riders',
                     'start_time_hour': 'Time (in Hours)'},
            hover_name='member_casual', hover_data={'member_casual': False, 'ride_length': True},
             color_discrete_map={'casual': '#FF7F00', 'member': '#008B8B'})
fig.show()
