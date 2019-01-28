import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

weather = pd.read_csv('../data/clean/all.csv')
cols = [ 'Temperature', 'Humidity','Pressure','Wind_direction', 'Wind_speed','Traffic_count']
weather = weather.filter(items = cols)
weather = (weather - weather.mean()) / (weather.max() - weather.min())


weather.to_csv('../data/clean/all_norm.csv',index = False)
# t = list(weather['Temperature'])
# traf = list(weather['Traffic_count'])
#
# plt.scatter(t,traf)
# plt.show()