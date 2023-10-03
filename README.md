<b>Author:</b> Tejaswini Sundar

<b><i>Date:</i></b> October, 2023
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

Insert folder overview photo here

The available data is in wide format, and follows the ROCCC approach:
* **Reliability:** This dataset is from the program in Chicago called Divvy, which includes complete and accurate data of the Chicago Department of Transportation (CDOT), which owns the city's bikes, stations, and vehicles.
* **Original:** The dataset is original as it was made available by Motivate International Inc, which operates the city of Chicago's bike-sharing program.
* **Comprehensive:** The dataset includes types of bikes, starting and ending stations names, station ID, station longitude and latitude, membership types.
* **Current:** data is up to date as of July 2023.
* **Cited:** the data is cited and under [license agreement](https://divvybikes.com/data-license-agreement).

The dataset is limitations:
* Personally identifiable information: data-privacy issues prohibit me from using riders' personal identifiable information, so from the CSV files, we have no data if a rider is a unique rider or not.
* NA values: after checking 
