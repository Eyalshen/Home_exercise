import pandas as pd
import datetime
from suntime import Sun
from matplotlib import pyplot as plt


# TODO: clean the code
# TODO: documantation
# TODO: matplotlib

# this function get suntime dictionary , sun object , timestamp , location
# and returns suntime of the location and date
def get_suntime(suntime_dict, sun, timestamp, location):
    date = get_RSD_date(int(timestamp))
    return get_suntime_by_given_location_and_date(suntime_dict, sun, location, date)


# this function gets location and date and returns the sunrise and sunset timestamp
# this method use dictionary to avoid of creating suntimes that was already created
def get_suntime_by_given_location_and_date(dict, sun, locations, date):
    if date not in dict.keys():
        sunrise = sun.get_local_sunrise_time(date)
        sunset = sun.get_local_sunset_time(date)
        sunrise_timestamp = sunrise.timestamp() * 1000
        sunset_timestamp = sunset.timestamp() * 1000
        dict[date] = (sunrise_timestamp, sunset_timestamp)
    return dict[date]


# This function get timestamp and returns the date
def get_RSD_date(timestamp):
    my_date = datetime.datetime.fromtimestamp(timestamp / 1000.0)
    return my_date.date()


# This method return if its night time
def is_daytime(suntime_dict, sun, timestamp, location):
    sunrise, sunset = get_suntime(suntime_dict, sun, timestamp, location)
    return (sunrise <= timestamp and timestamp <= sunset)


def initialize_sun_by_df_row(df_row):
    locations = df_row["location"]
    locations_list = locations.split(",")
    return Sun(float(locations_list[0]), float(locations_list[1]))



# this function get dataframe of RSDs and filtering out the
def filtering_out_night_RSDs(input_dataframe):
    sun = initialize_sun_by_df_row(input_dataframe.loc[0])
    suntime_dict = dict()

    input_dataframe["is day"] = [is_daytime(suntime_dict, sun, timestamp, location) for (timestamp, location) in
                             zip(input_dataframe['rsd_time'], input_dataframe['location'])]
    nighttime_df = input_dataframe.loc[input_dataframe["is day"] == False]

    # cleaning and restoring the DataFrame
    del input_dataframe['is day']
    del nighttime_df['is day']
    return nighttime_df



def plotting_df(dataframe, my_plot, i_color):
    list_dates = [get_RSD_date(timestamp) for timestamp in dataframe['rsd_time']]
    list_minutes = [rsd_time_to_plot(timestamp) for timestamp in dataframe['rsd_time']]
    my_plot.scatter(list_dates, list_minutes, s=0.5, color=i_color, alpha=0.6)



def rsd_time_to_plot(timestamp):
    my_date = (datetime.datetime.fromtimestamp(timestamp / 1000.0))
    date = my_date.date()
    minutes = my_date.time().hour * 60 + my_date.time().minute
    return minutes


if __name__ == '__main__':
    input_plot = plt
    plt.style.use('Solarize_Light2')
    df = pd.read_csv("Query_IL.csv")
    new_df = filtering_out_night_RSDs(df)
    # plotting_df(df, input_plot, "darkorange")
    # plotting_df(new_df, input_plot, "cornflowerblue")
    # input_plot.show()
