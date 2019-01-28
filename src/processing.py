import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
##############Weather##################
#import
temperature = pd.read_csv('../data/historical-hourly-weather-data/temperature.csv')
pressure = pd.read_csv('../data//historical-hourly-weather-data/pressure.csv')
weather_description = pd.read_csv('../data//historical-hourly-weather-data/weather_description.csv')
wind_speed = pd.read_csv('../data//historical-hourly-weather-data/wind_speed.csv')
humidity = pd.read_csv('../data//historical-hourly-weather-data/humidity.csv')
wind_direction = pd.read_csv('../data//historical-hourly-weather-data/wind_direction.csv')
#filter
weather_description = weather_description.filter(items=['datetime','New York'])
temperature = temperature.filter(items=['datetime','New York'])
pressure = pressure.filter(items=['datetime','New York'])
wind_speed = wind_speed.filter(items=['datetime','New York'])
humidity = humidity.filter(items=['datetime','New York'])
wind_direction = wind_direction.filter(items=['datetime','New York'])
#merge
weather = (weather_description.merge(temperature, on='datetime').
merge(humidity, on='datetime').
merge(pressure, on='datetime').
merge(wind_direction, on='datetime').
merge(wind_speed, on='datetime'))
weather.columns = ['Datetime','Description', 'Temperature', 'Humidity','Pressure','Wind_direction', 'Wind_speed']
weather = weather.fillna(method='ffill')
weather = weather.fillna(method='bfill')

weather = weather.set_index('Datetime')
weather.index = pd.to_datetime(weather.index)
weather.to_csv('../data/clean/weather_merge.csv')
discription = weather['Description'].resample('4H').last()
weather = weather.resample('4H').mean()
weather['Description'] = discription
weather = weather.loc[:, ['Description', 'Temperature', 'Humidity','Pressure','Wind_direction', 'Wind_speed']]
###############Traffic################
traffic  = pd.read_csv('../data/traffic/NYPD_Motor_Vehicle_Collisions.csv',usecols=['DATE','TIME'])
traffic['Datetime'] = traffic['DATE']+' '+traffic['TIME']
traffic['Traffic_count'] = 1
traffic = traffic.filter(items=['Datetime','Traffic_count'])
traffic = traffic.fillna(method='ffill')
traffic = traffic.fillna(method='bfill')
traffic['Datetime'] = pd.to_datetime(traffic['Datetime'])
traffic = traffic[(traffic['Datetime']>='2012-10-01 12:00:00') & (traffic['Datetime']<='2017-11-30 00:00:00')]
traffic = traffic.set_index('Datetime')
traffic = traffic.resample('4H').sum()
traffic.to_csv('../data/clean/NYPD_Motor_Vehicle_Collisions.csv')

weather = (weather.merge(traffic, on='Datetime'))
cols = [ 'Temperature', 'Humidity','Pressure','Wind_direction', 'Wind_speed','Traffic_count']
#outlier detection
for col in cols:
        Q1 = np.percentile(weather[col], 25)
        Q3 = np.percentile(weather[col],75)
        IQR = Q3 - Q1
        outlier_step = 1.5 * IQR
        weather = weather[(weather[col] > Q1 - outlier_step) & (weather[col] < Q3 + outlier_step )]
weather.to_csv('../data/clean/all.csv')