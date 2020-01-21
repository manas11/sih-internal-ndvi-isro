import rasterio
from rasterio import plot
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
from scipy.signal import argrelextrema
from scipy.ndimage import gaussian_filter
import random


values = [0.014040692487977192, 0.07890203420219506, 0.08509954026388375, -0.04759209718543126, 0.040521657276412944, 0.11806851682551592, 0.5218574705191966, -0.32317079952046796, -0.04610572553173446, 0.039493476478010325, -0.025335441441381244, -0.11764543079762999, 
        -0.04089301619266521, 0.12004972588485013, 0.003550960104030452, -0.122096000378005, 0.11486067431204061, 0.2360899083300908, 0.09149557386874313, 0.4961339780005558, -0.2054883838997877, 0.09069882654069987, -0.05272026451525333, -0.06322082544682465]
a = pd.DatetimeIndex(start='2017-01-15', end='2019-01-15', freq='M')
b = pd.Series(values, index=a)
fig, ax = plt.subplots()
ax.plot(b.index, b, label="line 1")
ndvis = values

for i in range(0, len(ndvis)-2):
    if abs(ndvis[i+1]-ndvis[i]) <= 0.20*ndvis[i]:
        ndvis[i+1] = ((ndvis[i] + ndvis[i+2])/2.0)
c = pd.Series(ndvis, index=a)
ax.plot(c.index, c, label="line 2")
c_gaus = gaussian_filter(c, sigma=0.7)
ax.plot(c.index, c_gaus, label="line 3")
ax.legend()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.show()
tf = np.array(ndvis)
# print(tf)
