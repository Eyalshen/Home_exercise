import datetime
import pandas as pd
import datetime
import suntime
import matplotlib
from suntime import Sun, SunTimeException
import time
import matplotlib.pyplot as plt
import numpy as np


def get_suntime(i_suntime_dict, i_sun, i_timestamp, i_location):
    date = get_RSD_date(int(i_timestamp))
    return get_suntime_by_given_location_and_date(i_suntime_dict, i_sun, i_location, date)


# this function gets location and date and returns the sunrise and sunset timestamp
def get_suntime_by_given_location_and_date(i_dict, i_sun, i_locations, i_date):
    if i_date not in i_dict.keys():
        sunrise = i_sun.get_sunrise_time(i_date)
        # sunrise = i_sun.get_local_sunrise_time(i_date)
        sunset = i_sun.get_sunset_time(i_date)
        # sunset = i_sun.get_local_sunset_time(i_date)



        sunrise_timestamp = sunrise.timestamp() * 1000
        sunset_timestamp = sunset.timestamp() * 1000
        i_dict[i_date] = (sunrise_timestamp,sunset_timestamp)
    return i_dict[i_date]


# This function get timestamp and returns the date
def get_RSD_date(i_timestamp):
    my_date = datetime.datetime.fromtimestamp(i_timestamp / 1000.0)
    return my_date.date()


# This method return if its night time
def is_daytime(i_suntime_dict, i_sun, i_timestamp , i_location):
    sunrise, sunset = get_suntime(i_suntime_dict, i_sun, i_timestamp, i_location)
    if sunrise <= i_timestamp and i_timestamp <= sunset:
        return True
    return False


def initialize_sun_by_df_row(i_df_row):
    locations = i_df_row["location"]
    locations_list = locations.split(",")
    return Sun(float(locations_list[0]), float(locations_list[1]))


def filtering_out_night_RSDs(i_dataframe):
    sun = initialize_sun_by_df_row(i_dataframe.loc[0])
    suntime_dict = dict()
    i_dataframe["is day"] = [is_daytime(suntime_dict, sun, timestamp, location) for (timestamp, location) in zip(i_dataframe['rsd_time'], i_dataframe['location'])]
    # creating nighttime_df
    nighttime_df = i_dataframe.loc[i_dataframe["is day"] == False]
    # cleaning and restoring the DataFrame
    del i_dataframe['is day']
    del nighttime_df['is day']
    return nighttime_df


def get_df_to_plot(input_df, output_df):
    plotting_df(input_df, "darkorange")
    plotting_df(output_df, "cornflowerblue")
    plt.show()


def plotting_df(i_dataframe, i_color):
    list_dates = [get_RSD_date(timestamp) for timestamp in i_dataframe['rsd_time']]
    list_minutes = [rsd_time_to_plot(timestamp) for timestamp in i_dataframe['rsd_time']]
    plt.scatter(list_dates, list_minutes, s=1, color=i_color)


def rsd_time_to_plot(i_timestamp):
    my_date = datetime.datetime.fromtimestamp(i_timestamp / 1000.0)
    date = my_date.date()
    time = my_date.time()
    total_minutes = time.hour * 60 + time.minute
    return total_minutes

df = pd.read_csv("Query_DE.csv")

new_df = filtering_out_night_RSDs(df)
print(new_df)

get_df_to_plot(df,new_df)
# print(df)

# TODO: clean the code
# TODO: exceptions
# TODO: documantation
# TODO: matplotlib

