import pandas as pd
import datetime
from suntime import Sun
from matplotlib import pyplot as plt

'''
program explanation :
* The program getting csv of RSDs ,and using it to create data frame
* the program uses the function filter_out_night_RSDs to filtering out night time RSDs
* the program also uses the function plot_DF to prepare the plot 
* the program uses some assumptions :
    1.  Each data frame will have those fileds : "rsd_time" , "location" :
        - This assumption uses to manipulate and filter the data frame 
    2.  All the locations of the RSDs are close to each other
        - This assumption leads us to create single sun Object
    3.  The data contains about 1 million RSDs from a range of about 180 days
        - This assumption leads us to use dynamic dictionary of suns times by the following rules : 
             * searching for suns time by given date in the dictionary
             * if  suns time was found then return it
             * else create the suns time of given date and insert it to the dictionary 
'''



def get_suntime_by_location_and_date(dict, sun, timestamp):
    # this function gets sun times dictionary ,sun object , timestamp and location returns the sunrise and sunset timestamp
    # this method uses dictionary to avoid searching of suntimes that were already created
    date = get_RSD_date(int(timestamp))
    if date not in dict.keys():
        sunrise = sun.get_local_sunrise_time(date)
        sunset = sun.get_local_sunset_time(date)
        sunrise_timestamp = sunrise.timestamp() * 1000
        sunset_timestamp = sunset.timestamp() * 1000
        dict[date] = (sunrise_timestamp, sunset_timestamp)
    return dict[date]


def get_RSD_date(timestamp):
    # This function get timestamp and returns the date
    my_date = datetime.datetime.fromtimestamp(timestamp / 1000.0)
    return my_date.date()


def is_daytime(suntime_dict, sun, timestamp):
    # This method return if its day time
    sunrise, sunset = get_suntime_by_location_and_date(suntime_dict, sun, timestamp)
    return sunrise <= timestamp and timestamp <= sunset


def initialize_sun_by_df_row(df_row):
    locations = df_row["location"]
    locations_list = locations.split(",")
    return Sun(float(locations_list[0]), float(locations_list[1]))


def filter_out_night_RSDs(input_dataframe):
    # this function gets a dataframe of RSDs and filters out the night RSDs
    sun = initialize_sun_by_df_row(input_dataframe.loc[0])
    suntime_dict = dict()

    input_dataframe["is day"] = [is_daytime(suntime_dict, sun, timestamp) for (timestamp) in
                                 input_dataframe['rsd_time']]
    daytime_dataframe = input_dataframe.loc[input_dataframe["is day"] == True]

    # cleaning and restoring the DataFrame
    input_dataframe = input_dataframe.drop(columns=['is day'])
    daytime_dataframe = daytime_dataframe.drop(columns=['is day'])

    return daytime_dataframe

def plot_DF(dataframe, my_plot, i_color):
    # This function gets dataframe , plot , color and preparing the plot to show
    plot_list = [rsd_time_to_plot(timestamp) for timestamp in dataframe['rsd_time']]
    my_plot.scatter(*zip(*plot_list), s=0.5, color=i_color, alpha=0.6)

def rsd_time_to_plot(timestamp):
    # This function get timestamp and returns tuple of date and minutes
    my_date = (datetime.datetime.fromtimestamp(timestamp / 1000.0))
    date = my_date.date()
    minutes = my_date.time().hour * 60 + my_date.time().minute
    return (date,minutes)


if __name__ == '__main__':
    input_plot = plt
    plt.style.use('Solarize_Light2')
    df = pd.read_csv("Query_IL.csv")
    new_df = filter_out_night_RSDs(df)
    # print(new_df)
    plot_DF(df, input_plot, "cornflowerblue")
    plot_DF(new_df, input_plot, "darkorange")
    input_plot.show()
