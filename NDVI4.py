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

def convert(f1,f2):
	#import bands as separate 1 band raster
	band5 = rasterio.open(f1) #nir
	band4 = rasterio.open(f2) #red

	#generate nir and red objects as arrays in float64 format
	red = band4.read(1).astype('float64')
	nir = band5.read(1).astype('float64')
	#ndvi calculation, empty cells or nodata cells are reported as 0
	ndvi=np.where((nir+red)==0., 0, (nir-red)/(nir+red))
	print('----------')
	# print(len(ndvi),'-',len(ndvi[0]))
	# print('----------')
	# print(ndvi)
	ctr=0
	n=0
	for i in ndvi:
		for j in i:
			if j>=0.3:
				ctr=ctr+j;
				n=n+1
	print('----------')
	return (ctr)



def plot(values):
	a = pd.DatetimeIndex(start='2017-01-15',end='2019-01-15' , freq='M')
	b = pd.Series(values, index=a)
	fig, ax = plt.subplots()
	ax.plot(b.index, b, label = "line 1")
	ndvis = values

	for i in range(0,len(ndvis)-2):
		if abs(ndvis[i+1]-ndvis[i]) <= 0.20*ndvis[i]:
			ndvis[i+1] = ((ndvis[i] + ndvis[i+2])/2.0)
	c = pd.Series(ndvis, index=a)
	ax.plot(c.index, c, label = "line 2")
	c_gaus = gaussian_filter(c, sigma=1.2)
	ax.plot(c.index, c, label="line 2")
	ax.plot(c.index, c_gaus, label="line 3")
	# t = [random.random()*1000 for _ in range(24)]
	# d = pd.Series(t, index=a)
	# ax.plot(d.index, d, label = "line 3")
	ax.legend()

	ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
	plt.show()
	tf= np.array(ndvis)
	print(tf)


def smooth(y, box_pts):
	box = np.ones(box_pts)/box_pts
	y_smooth = np.convolve(y, box, mode='same')
	return y_smooth
	

def main():
	files = glob.glob("/home/bharath/Desktop/Clipped_NDVI/*")
	files.sort()
	print(files)
	n = len(files)
	ndvis = []
	for i in range(0,n,2):
		print('Files are = ',files[i],files[i+1])
		ndvis.append(convert(files[i],files[i+1]))

	print("NDVI VALUES")		
	print(ndvis)
	plot(ndvis)
	print('-----')
	


if __name__ == "__main__": 
	main()
