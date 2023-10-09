<b>Author:</b> Tejaswini Sundar

<b><i>Date:</i></b> 9th October, 2023
# Google Data Analytics Capstone: Cyclistic Bike-Share Analysis
In this case study analysis, I will be taking on the role of a junior data analyst working for the marketing team at a fictional company, Cyclistic, as mentioned in the [Google Data Analytics Course Capstone](https://www.coursera.org/learn/google-data-analytics-capstone). As the director believes that the company's future success depends on maximising the number of annual memberships, I am tasked with understanding how casual riders and annual members use Cyclistic bikes. In short, the goals I have to achieve in this case study include:

## Goals:
- Use Cyclistic's historical data to obtain insights on the use of Cyclistic bikes by casual riders and annual members.
- Design marketing strategies aimed at converting casual riders into annual members.
- Discuss your findings with key stakeholders.

The public dataset that I will be using is [Cyclistic's historical trip data](https://divvy-tripdata.s3.amazonaws.com/index.html), which is made available by Motivate International Inc. under a license. For the purposes of this case study, the datasets have been made appropriate, and no credit card details have been utilised to maintain consumers' data-privacy issues. Additionally, for a deeper dive into the case study, I will work with a year's worth of data, from August 2022 to July 2023, given that I am working on this case study in 2023.

## Introduction - About Cyclistic
Cyclistic successfully launched a bike-share offering in 2016, with the program growing to have a fleet of 5,824 geotracked bicycles that are locked into a network of 692 stations across Chicago. The company sets itself apart by offering reclining bikes, hand tricycles, and cargo bikes, making it more inclusive for the differently-abled and riders who can't use the standard two-wheeled bike. While most riders use these bikes for leisure, about 30% of the riders use it to commute to work.

Until now, the marketing strategy for the company relied mainly on building general awareness and appealing to broad consumer segments, with one of their plans being to come up with flexible pricing plans that move along the lines of issuing single-ride and full-day passes alongside annual memberships. Although the company receives most of its profits from its single and full-day pass users, the director believes that increasing the number of annual members in the company will help drive future growth. 

For this case study, I will be following the steps of the data analysis process, which are [Ask](#ask), [Prepare](#prepare), [Process](#process), [Analyse](#analyse), [Share](#share), and [Act](#act).

## Ask:
The director, Lily Moreno, has addressed three driving questions for the future marketing programs, which are:
1. How do annual members and casual riders use Cyclistic bikes?
2. Why would casual riders buy Cyclistic annual memberships?
3. How can Cyclistic use digital media to influence casual riders to become members?

Moreno has assigned me the first question, which is now my business task:
### Business Task:
Find the difference in usage of Cyclistic's bikes between annual members and casual riders.
As mentioned above, I will be using the company's historical data (Aug 2022 - Jul 2023) to produce my reports and analysis. From this question, I will be able to pinpoint variations to current changes in marketing strategy, and how we as a company can target casual riders to convert them to annual members.

The primary stakeholders in the project are:
- **Lily Moreno:** Director of marketing, my manager. Responsible for development of campaigns and initiatives.
- **Cyclistic executive team:** the team responsible for approving recommended marketing programs.

The secondary stakeholders in the project are:
- **Cyclistic marketing analytics team:** team of data analysts responsible for collecting, analysing, and reporting data to guide marketing strategy.

## Prepare:
The dataset used to analyse Cyclistic's bike sharing program consist of 12 CSV files, spanning August 2022 to July 2023. Before keeping the filenames readable and consistent, I organised the files into a separate folder, labelled CSV Files under the Cyclistic_Files folder. A screenshot of the same is given below:

![Screenshot of the organised data within the Cyclistic Files](/Final_Screenshots/Folder_Overview.png?raw=true "Cyclistic Folder")

The available data is in wide format, and follows the ROCCC approach:
* **Reliability:** This dataset is from the program in Chicago called Divvy, which includes complete and accurate data of the Chicago Department of Transportation (CDOT), which owns the city's bikes, stations, and vehicles.
* **Original:** The dataset is original as it was made available by Motivate International Inc, which operates the city of Chicago's bike-sharing program.
* **Comprehensive:** The dataset includes types of bikes, starting and ending stations names, station ID, station longitude and latitude, membership types.
* **Current:** data is up to date as of July 2023.
* **Cited:** the data is cited and under [license agreement](https://divvybikes.com/data-license-agreement).

The dataset is limitations:
* Personal information: data-privacy issues prohibit me from using riders' personal identifiable information, so from the CSV files, we have no data to support the existence of unique riders.
* Missing values: using ```isna().sum()``` to count the number of missing values within the final merged CSV files before we begin the processing stage, we find that the columns relating to starting and ending stations, including both name and ID have approximately 86.8k - 92.5k missing values. This also extends to the stations latitude and longitude, which we will exclude for the purposes of the analysis.

```
final_file.isna().sum()
final_file.dropna(inplace=True)
```

## Process
After downloading the required CSV files from Aug '22 - Jul '23, I loaded and installed the necessary packages on PyCharm, after which I created data frames that read data from the CSV files before merging them into one big file for easier processing.

```
import pandas as pd
import plotly.express as px
from plotly.offline import init_notebook_mode

init_notebook_mode(connected=True)
import plotly.io as pio

import matplotlib.pyplot as plt
import seaborn as sea

final_file = pd.concat([aug_2022, sept_2022, oct_2022, nov_2022, dec_2022, jan_2023, feb_2023,
                        mar_2023, apr_2023, may_2023, jun_2023, jul_2023],
                       ignore_index=True)
```

Before I begin the analysing phase, I will delete columns that I will not be using during the analysis, such as starting and ending station IDs, the ending station's name, and related geographical coordinates:

```
final_file = final_file.drop(['start_station_id', 'end_station_id', 'end_station_name',
                              'start_lat', 'start_lng', 'end_lat', 'end_lng'], axis=1)
```

A closer look into the available data shows that the datatype for the starting and ending dates for each ride is in a datatype other than datetime. 

```
final_file['started_at'] = final_file['started_at'].astype('datetime64[ns]')
final_file['ended_at'] = final_file['ended_at'].astype('datetime64[ns]')
```

I also added a column called "ride_length" that indicates the minutes spent in a ride (either casual or member). I then removed records containing negative ride_length values.

```
final_file['ride_length'] = (final_file['ended_at'] - final_file['started_at']) / pd.Timedelta(minutes=1)
final_file['ride_length'] = final_file['ride_length'].astype('int32')

final_file[final_file['ride_length'] < 0].count()

final_file = final_file[final_file['ride_length'] > 0]
final_file = final_file.reset_index()
final_file = final_file.drop(columns='index')
```

After converting the date columns into datetime datatype, I populated the respective day, month, year, and the hour into separate columns for easier analysis:

```
final_file['start_date'] = final_file['started_at'].dt.day
final_file['start_time_hour'] = final_file['started_at'].dt.hour
final_file['start_day_of_week'] = final_file['started_at'].dt.day_name()
final_file['start_month'] = final_file['started_at'].dt.month_name()
final_file['start_year'] = final_file['started_at'].dt.year
```

After checking for unique and duplicate values in the final merged file, I created a separate CSV file in the folder that held the processed file from where I began my analysis. A quick look into the file shows that the days of the week and the targeted months have not been ordered properly, so placing them both in accordance with my requirements, which is ordering the days from Monday - Sunday and the months from August to July.

```
days_of_the_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
final_file_clean['start_day_of_week'] = pd.Categorical(final_file_clean['start_day_of_week'],
                                                       categories=days_of_the_week_order, ordered=True)

month_order = ['August', 'September', 'October', 'November', 'December', 'January', 'February', 'March', 'April', 'May',
               'June', 'July']
final_file_clean['start_month'] = pd.Categorical(final_file_clean['start_month'], categories=month_order, ordered=True)
```

It should be noted that the days of the week mentioned in this file are days of the week where users began their rides. This column in the Python script is called ```start_day_of_week```. 

## Analyse
I begin my analysis with acquiring the percentage of users, and the average riding minutes spent per user within the dataset. Note that ```final_file_clean_1``` is the name the processed file from the previous stage on which I will be analysing my data.

```
percentage_users = round(final_file_clean['member_casual'].value_counts(normalize=True) * 100, 1)

final_file_clean_1 = final_file_clean.groupby('member_casual', as_index=False)['ride_length'].agg('mean')
print(final_file_clean_1)
```

Total Percentage of the Users

![Screenshot of the total percent of users](/Final_Screenshots/Total_percent_users.png?raw=true "Total percent users")

Total Percentage of bikes used

![Screenshot of the total percentage of bikes used](/Final_Screenshots/Average_Riding_Minutes_per_Rider.png?raw=true "Total percent of bikes used")

As observed above, I saw that the although the number of member riders was greater than the number of casual riders during the years 2022-2023 (Members - 62.8% and Casual Riders - 37.2%), the average time spent riding by casual riders was twice as long as that of the members, with casual riders spending an average of 22.31 minutes riding Cyclistic bikes and member riders spending half the amount, nearly 11.86 minutes.

Wanting to further investigate this dataset for more clues, I wanted to check the most preferred bike for each user within this period, using the below code:

```
percentage_bikes = round(final_file_clean['rideable_type'].value_counts(normalize=True) * 100, 1)
```

I noted that most users in the database preferred the Classic Bike (57.5% of users rode this bike around the city), the Electric Bike was preferred by 39.6%, and the number of docked bikes were rare occurrences, with the dataset only holding 2.9% of docked bikes. 

To prove my speculation, I noted the average riding lengths of the different users using various measures, including the insight based on a week, over 24 hours, and over 12 months. These were my obtained results:

```
avg_ride_length_per_user = final_file_clean.groupby(['member_casual', 'start_day_of_week']).ride_length.mean()

final_file_clean.groupby(['member_casual', 'start_time_hour']).ride_length.mean()

final_file_clean.groupby(['member_casual', 'start_month']).ride_length.mean()
```

Average Riding Minutes - Weekly View:

![Screenshot of the average riding minutes in a week](/Final_Screenshots/Avg_ride_length_per_day.png?raw=true "Average Riding Length in a Week")

Average Riding Minutes - Hourly View:

![Screenshot of the average riding minutes in a day](/Final_Screenshots/Avg_ride_length_per_day.png?raw=true "Average Riding Length in a Week")

Average Riding Minutes - Monthly View:

![Screenshot of the average riding minutes in a year](/Final_Screenshots/Avg_monthly_ride_length_per_user.png?raw=true "Average Riding Length in a Year")

We observe the following:

* A decrease in the average riding minutes of casual riders from Monday (~22.11 minutes) to Wednesday (~19 minutes)
  * This picks up as the week draws towards the weekends, from Thursday (19.61 minutes) to Sunday (~25.6 minutes).
  * We can speculate that most casual riders prefer taking Cyclistic bikes during the weekend for weekend trips.
* Member riders stay relatively consistent throughout the week, with a slight increase in the average riding minutes over the weekend.
  * The range is from 11.29 minutes, which is the lowest seen on Wednesday, and 13.41 minutes, seen on Saturday.
* The maximum riding time during a day, when viewed hourly, for casual riders is during the late hours of the morning to the early hours of the afternoon.
  * More precisely, it is from 10AM - 2PM
  * The average riding minutes during this time for casual riders is 26.42 minutes.
* The maximum riding time during a day for member riders is from 2PM - 8PM, where the average riding minutes was 12.36 minutes.
  * We can speculate that this is the occurrence when riders end their workshift during the workday.
* For casual riders, the months with the highest riding time is from April to July, with April averaging a riding time of 22.61 minutes and July averaging 25.17 minutes.
  * This decreases when the colder months begin.
  * The highest average riding minutes during this period is July, with 25.17 minutes as riding average.
* As for member riders, the months with the highest riding time is from May to September, with average riding times of 12.5 minutes and 12.38 minutes respectively.
  * The highest average riding minute during these months was also July, with 13.128 minutes as riding average.

Additionally, I wanted to find the top 5 busiest stations that were starting points for casual riders for a better, more customer-centric marketing strategy. 

```
n = 5
top_5_station_names = final_file_clean['start_station_name'].value_counts()[:n].index.to_list()
```

I found that the busiest stations were:
1. Streeter Dr & Grand Ave
2. DuSable Lake Shore Dr & Monroe St
3. Michigan Ave & Oak St
4. DuSable Lake Shore Dr & North Blvd
5. Clark St & Elm St

Also, if we try to link the average riding time per user to the offered bikes, we find that: 
* The minutes casual riders spent riding was highest for docked bikes (49.44 minutes) and followed by classic bikes following second (24.38 minutes) and electric bikes at (14.94 minutes).
* Member riders preferred classic bikes (12.73 minutes) to electric bikes (10.41 minutes). There was no instance of docked bikes for member riders.

To gain more insight into my dataset, I tried to count the number of rides per user along with the bikes Cyclistic offered. I obtained the following results using the below code:

```
final_file_clean_6 = final_file_clean.groupby(['member_casual', 'rideable_type'])['ride_id'].count().rename_axis(
    ['member_casual', 'rideable_type']).reset_index(name='count')
```

Similarly, I found the number of rides of each user in the dataset based on month, hour, and the starting day of the week. I also found the number of rides from the top 5 stations mentioned above. Here are the attached screenshots and my observations.

Count of Bike Rides per User - Monthly View:

![Screenshot of the bike rides in a year](/Final_Screenshots/Monthly_bike_rides_per_user.png?raw=true "Count of Bike Rides per User in a Year")

Count of Bike Rides per User - Hourly View:

![Screenshot of the bike rides in a day](/Final_Screenshots/Hourly_bike_rides_per_user.png?raw=true "Count of Bike Rides per User in a Day")

Count of Bike Rides per User - Daily View:

![Screenshot of the bike rides in a week](/Final_Screenshots/Count_of_Daily_bike_rides_per_user.png?raw=true "Count of Bike Rides per User in a Week")

Count of Bike Rides per User - Station View:

![Screenshot of the bike rides in each station](/Final_Screenshots/Max_rides_per_station_per_user.png?raw=true "Count of Bike Rides per User in each station")

### Observations:
1. Classic bikes (clocking 776,921 rides) and electric bikes (679,247 rides) were mostly preferred by casual riders, with the number of docked bikes at (124,848 occurrences).
  i. Member bikes also prefer classic bikes (1,665,796 rides) to electric bikes (1,003,235 rides). There is no occurrence of docked bikes for member riders.
2. The ride count for casual riders increases from April (108,163 rides) to August (265,748 rides) before decreasing as the colder months of the year begin.
  i. Member riders clock in more rides as compared to casual riders, with the highest number of rides being 328,577 in August.
  ii. This can be seen occuring over a period of April (206,758 rides) to August, which is far greater than the number of rides of casual riders.
3. Looking into the hourly interpretation of the count of rides for both casual and member riders, I found that:
  i. Casual riders take more rides during the afternoon to evening hours of a day (101,429 rides at noon to 155,512 rides at 6PM). This spans over an hourly period of 6 hours.
  ii. Member riders take more rides during the morning hours till the early hours of the night (149,515 at 7AM and 109,135 at 8PM), which could mean a full utilisation of Cyclistic bikes for the duration of their membership.
  iii. Member riders use their bikes for nearly 13 hours a day.
4. The highest number of rides in a week by casual riders is 322,425 on Saturday, while the highest number of rides being Wednesday for member riders (429,854 rides).
  i. The number of rides by member riders remains consistently higher than casual riders.
5. For casual riders, I notice that the busiest starting stations are Streeter Dr & Grand Ave, with 46,278 rides, and Kingsbury ST & Kinzie St 22,917 rides.

## Share
To share my ideas with the primary and secondary stakeholders, I created a [dashboard using Tableau](https://public.tableau.com/views/GoogleDataAnalyticsCapstone-Cyclistic_16966057338790/Dashboard1?:language=en-US&:display_count=n&:origin=viz_share_link) that contains the highlighted visuals for easier understanding, some of which I would also be using in my [presentation](https://docs.google.com/presentation/d/e/2PACX-1vSVViTzXi8smzDqdcoK7m4Ufmwkcfa2rsRQtLtoZSf6iDJPqWgLQtE803EIKaaWo92oPkstzlSNZDyE/pub?start=false&loop=false&delayms=3000).

## Act
And now, the final step of the data analysis process! From the above analysis, I would like to restate the objectives of the analysis once again before I dive into my proposed high-level solutions to the director and the Cyclistic Executive Team:

- Use Cyclistic's historical data to obtain insights on the use of Cyclistic bikes by casual riders and annual members.
- Design marketing strategies aimed at converting casual riders into annual members.
- Discuss your findings with key stakeholders.

As requested by the director, here are the following marketing strategies that I recommend:
1. Create marketing adverts for casual riders with weekend packages to touristic destinations tie-ups in and around the city for a specific period. Rides taken during this period can be used to discount the membership amount for a maximum trial period of two months before helping the casual rider become a full-time member of Cyclistic.
2. Create marketing packages that use the number of rides taken by casual riders to avail gift cards to sporting goods, converting their rides to a point-based system to obtains discounts on apparel and related gear before shifting to a two-month membership trial period.
3. Could also push for trial memberships based on the number of rides taken by casual riders, which if availed during a promotional week, they can sign up for memberships at discounted prices.
4. Link the number of rides taken at the top 5 busiest stations to offer further discounts on memberships. This can be done with the point-based system and the ID of the starting station, to come up with marketing strategies like "5 continuous rides at Station X will give you a discounted price on a two-month trial period of the membership".

This concludes my analysis! Hope this helps!
