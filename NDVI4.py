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
from scipy.signal import argrelextrema
from scipy.ndimage import gaussian_filter
import random
from scipy.signal import find_peaks
from scipy.signal import argrelextrema
import statsmodels.api as sm
import matplotlib
from statsmodels.tsa.seasonal import seasonal_decompose


def convert(f1,f2):
	#import bands as separate 1 band raster
	band5 = rasterio.open(f1) #nir
	band4 = rasterio.open(f2) #red

	#generate nir and red objects as arrays in float64 format
	red = band4.read(1).astype('float64')
	nir = band5.read(1).astype('float64')
	#ndvi calculation, empty cells or nodata cells are reported as 0
	ndvi=np.where((nir+red)==0., 0, (nir-red)/(nir+red))
	ctr=0
	n=0
	for i in ndvi:
		for j in i:
			if j>=0.3:
				ctr=ctr+j;
				n=n+1
	return (ctr)

def plot(values):

	a = pd.date_range(start='15/1/2017', end='15/01/2019', freq = 'M')
	b = pd.Series(values, index=a)
	peaks_raw = crop_parameters(values)
	np_values = np.array(values)
	minima_raw = argrelextrema(np_values, np.less)
	fig, ax = plt.subplots()
	ax.plot(b.index, b, label = "Raw")
	ax.plot(a[peaks_raw], np_values[peaks_raw], "x")
	ax.plot(a[minima_raw], np_values[minima_raw], "o")
	plt.show()
	print('Raw Data')
	print('Number of Harvests raw data = ', a[peaks_raw])
	print('Minimas Raw =', a[minima_raw])

	sleep = input("Press any key to Continue")



	# 20% Threshold
	ndvis = values
	for i in range(0,len(ndvis)-2):
		if abs(ndvis[i+1]-ndvis[i]) <= 0.20*ndvis[i]:
			ndvis[i+1] = ((ndvis[i] + ndvis[i+2])/2.0)
	np_ndvis = np.array(ndvis)
	peaks_20 = crop_parameters(ndvis)
	minima_20 = argrelextrema(np_ndvis, np.less)
	c = pd.Series(ndvis, index=a)
	fig, bx = plt.subplots()
	bx.plot(c.index, c, label = "20%")
	bx.plot(a[peaks_20], np_ndvis[peaks_20], "x")
	bx.plot(a[minima_20], np_ndvis[minima_20], "o")
	plt.show()
	print('After 20% Threshold')
	print('Number of Harvests after 20% Threshold = ', a[peaks_20])
	print('Minimas 20% =', a[minima_20])


	sleep = input("Press any key to Continue")

	# Applying Gaussian Distribution
	c_gaus = gaussian_filter(c, sigma=1.3)
	c_gaus_list = c_gaus.tolist()
	d = pd.Series(c_gaus_list, index=a)
	minima_gauss = argrelextrema(np.array(c_gaus_list), np.less)
	peaks_gaus = crop_parameters(c_gaus_list)
	fig, cx = plt.subplots()
	cx.plot(d.index, d, label="Gaussian")
	cx.plot(a[peaks_gaus], c_gaus[peaks_gaus], "x")
	cx.plot(a[minima_gauss], c_gaus[minima_gauss], "o")
	plt.show()
	print('Peaks after gaussian_filter')
	print('Peaks after gaussian_filter = ', a[peaks_gaus])
	print('Minimas Gaus =', a[minima_gauss])

	print('Date of Sowing after Gaussian')
	print('First = ',a[0])
	print('Second = ', a[minima_gauss])
	print('Date of Harvesting after Gaussian')
	print(a[peaks_gaus])



	sleep = input("Press any key to Continue")

	decomposition = sm.tsa.seasonal_decompose(b, model = 'additive')
	fig = decomposition.plot()
	matplotlib.rcParams['figure.figsize'] = [9.0, 5.0]
	plt.show()

	sleep = input("Press any key to Continue")

	decomposition = sm.tsa.seasonal_decompose(c, model = 'additive')
	fig = decomposition.plot()
	matplotlib.rcParams['figure.figsize'] = [9.0, 5.0]
	plt.show()

	sleep = input("Press any key to Continue")

	decomposition = sm.tsa.seasonal_decompose(d, model = 'additive')
	fig = decomposition.plot()
	matplotlib.rcParams['figure.figsize'] = [9.0, 5.0]
	plt.show()

	# fig, axes = plt.subplots(1,3, figsize=(20,4), dpi=100)
	# pd.read_csv(, parse_dates=['date'], index_col='date').plot(title='Seasonality Only', legend=False, ax=axes[1])
	# plt.show()

	


def crop_parameters(ndvis):
	peaks, _ = find_peaks(ndvis, height=0)
	return peaks


def main():
	files = glob.glob("/home/stark/SIH/sih-isro/Clipped_NDVI/*")
	files.sort()
	n = len(files)
	ndvis = []
	print('PROCESSING FILES AND CONVERTING IT TO NDVI')
	for i in range(0,n,2):
		# print('Files are = ',files[i],files[i+1])
		ndvis.append(convert(files[i],files[i+1]))

	plot(ndvis)
	print('-----')
	


if __name__ == "__main__": 
	main()
