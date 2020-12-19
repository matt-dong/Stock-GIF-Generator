# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 22:28:15 2020

@author: mattd
"""

import matplotlib.animation as ani
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# import data
csv_filename = "TSLA.csv" # Robinhood users holding
df = pd.read_csv(csv_filename)
csv_filename = "AV_TSLA.csv" # stock prices from AlphaVantage
av_df = pd.read_csv(csv_filename)

# convert timestamp to datetime and set it as index
df["timestamp"] = pd.to_datetime(df["timestamp"])
df.index = df["timestamp"]
df = df.drop(["timestamp"], axis=1)

av_df["timestamp"] = pd.to_datetime(av_df["timestamp"])
av_df.index = av_df["timestamp"]
av_df = av_df.drop(["timestamp"], axis=1)

# resample index to daily
df = df.resample('D').mean()

# ensure indixes of 2 dfs match
av_df = av_df.iloc[::-1]
av_df = av_df.loc[df.index[0]:df.index[len(df)-1]]


# merge dfs and drop unnecessary columns
df = pd.concat([df, av_df], axis=1, join='inner')
for col in df.columns:
    if not col == "users_holding" and not col == "adjusted_close":
        df = df.drop([col], axis=1)
        
# setup plt with 2 axes
fig = plt.figure()
ax1 = fig.add_subplot(111)
line1 = ax1.plot(df.index, df['users_holding'], color='g')
ax2 = ax1.twinx()
line2 = ax2.plot(df.index, df['adjusted_close'], color='b')

lines = line1+line2
labels = [l.get_label() for l in lines]


# create animation
# define the function animate, which has the input argument of i:
def animate(i):
  data =  df.iloc[:int(i+1)]  #select data range
  xp = []
  yp = []
  zp = []
  
  lines = data

  for line in lines:
    xp = data.index
    yp = data['users_holding']
    zp = data['adjusted_close']

  # clear ax(1):
  ax1.clear()
  ax2.clear()
  
  # plot axis 1
  line1 = ax1.plot(xp, yp, color = 'g')
  # plot axis 2   
  line2 = ax2.plot(xp, zp, color = 'b')
  line = line1+line2
  # set legend in top left corner
  plt.legend(line, df.columns, loc = "upper left")

  # provide a label for the x-axis:
  ax1.set_xlabel('date')
  ax1.set_ylabel('users holding', color='g')
  ax1.tick_params(axis='y', labelcolor='g')
  # provide a label for the y-axis:  
  ax2.set_ylabel('stock price', color='b')
  ax2.tick_params(axis='y', labelcolor='b')

# animate gif and save   
anim = ani.FuncAnimation(fig, animate, interval = 200, frames = 1500)
anim.save('TSLA.gif', writer='imagemagick')
plt.show()

        