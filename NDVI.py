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
			n = n+1
			if j>=0.3:
				ctr=ctr+j;
	return ctr, n

def peak_between_minima(list_peaks_seasonal,list_minimas_seasonal):
	no_of_crop_cycles = 0
	peak_start_index = 0
	minima_start_index = 0
	while (peak_start_index < len(list_peaks_seasonal)) and (minima_start_index < len(list_minimas_seasonal)-1):
		if (list_peaks_seasonal[peak_start_index] >= list_minimas_seasonal[minima_start_index]) and (list_peaks_seasonal[peak_start_index] <= list_minimas_seasonal[minima_start_index+1]):
			no_of_crop_cycles += 1
			peak_start_index += 1
			minima_start_index += 1
		elif list_peaks_seasonal[peak_start_index] < list_minimas_seasonal[minima_start_index]:
			peak_start_index += 1
		elif list_peaks_seasonal[peak_start_index] > list_minimas_seasonal[minima_start_index + 1]:
			minima_start_index += 1
	print('Number of crop cycles:', no_of_crop_cycles)

def plot(values):

	extra = pd.date_range(start='15/1/2017', end='15/01/2019', freq = 'M')
	a = pd.date_range('2017-01-01', periods=len(values), freq='MS') + pd.DateOffset(days=14)
	b = pd.Series(values, index=a)
	peaks_raw = crop_parameters(values)
	np_values = np.array(values)
	minima_raw = argrelextrema(np_values, np.less)
	fig, ax = plt.subplots()
	ax.plot(b.index, b, label = "Raw")
	ax.plot(a[peaks_raw], np_values[peaks_raw], "x")
	ax.plot(a[minima_raw], np_values[minima_raw], "o")
	plt.show()
	print('Raw Data:')
	print('Dates of Harvesting:', a[peaks_raw].strftime(
		'%d-%m-%Y').str.cat(sep=', '))
	print('Dates of Sowing:', a[minima_raw].strftime(
		'%d-%m-%Y').str.cat(sep=', '))

	sleep = input("Press any key to continue")

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
	print('After applying 20% Threshold:')
	print('Dates of Harvesting:', a[peaks_20].strftime(
		'%d-%m-%Y').str.cat(sep=', '))
	print('Dates of Sowing:', a[minima_20].strftime(
		'%d-%m-%Y').str.cat(sep=', '))

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
	print('After applying Gaussian Filter:')
	print('Dates of Harvesting:', a[peaks_gaus].strftime(
		'%d-%m-%Y').str.cat(sep=', '))
	print('Dates of Sowing:', a[minima_gauss].strftime(
		'%d-%m-%Y').str.cat(sep=', '))

	sleep = input("Press any key to Continue")

	e = pd.Series(c_gaus_list, index=extra)
	decomposition = sm.tsa.seasonal_decompose(e, model = 'additive')
	fig = decomposition.seasonal.plot()
	matplotlib.rcParams['figure.figsize'] = [9.0, 5.0]
	plt.show()

	minimas_seasonal = argrelextrema(np.array(decomposition.seasonal), np.less)
	peaks_seasonal = crop_parameters(decomposition.seasonal)
	
	list_peaks_seasonal = list(peaks_seasonal)
	list_minimas_seasonal = list(minimas_seasonal[0])
	peak_between_minima(list_peaks_seasonal,list_minimas_seasonal)
	sleep = input("Press any key to Continue")
	

def crop_parameters(ndvis):
	peaks, _ = find_peaks(ndvis, height=0)
	return peaks


def main():
	files = glob.glob("../Clipped_NDVI/*")
	files.sort()
	n = len(files)
	ndvis = []
	crop_percentage = []
	print('PROCESSING FILES AND CONVERTING IT TO NDVI')
	for i in range(0,n,2):
		# print('Files are = ',files[i],files[i+1])
		x,y = convert(files[i],files[i+1])
		ndvis.append(x)
		crop_percentage.append((x/y)*100)

	plot(ndvis)
	print('-----')
	a = pd.date_range('2017-01-01', periods=len(ndvis), freq='MS') + pd.DateOffset(days=14)
	b = pd.Series(crop_percentage, index=a)
	print('CROP PERCENTAGE')
	print(b)



if __name__ == "__main__": 
	main()
