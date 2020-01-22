#import required libraries
import os
import rasterio
from rasterio import plot
import matplotlib.pyplot as plt
import numpy as np

def generate_ndvi(path1, path2, title):
    os.listdir('../Clipped_NDVI/')
    #import bands as separate 1 band raster
    band4 = rasterio.open(path2)  # red
    band5 = rasterio.open(path1)  # nir
    #number of raster rows
    band4.height
    #number of raster columns
    band4.width
    #plot band
    # plot.show(band4)
    #type of raster byte
    band4.dtypes[0]
    #raster sytem of reference
    band4.crs
    #raster transform parameters
    band4.transform
    #raster values as matrix array
    band4.read(1)
    #generate nir and red objects as arrays in float64 format
    red = band4.read(1).astype('float64')
    nir = band5.read(1).astype('float64')

    nir
    #ndvi calculation, empty cells or nodata cells are reported as 0
    ndvi = np.where(
        (nir+red) == 0.,
        0,
        (nir-red)/(nir+red))
    ndvi[:5, :5]
    #export ndvi image
    ndviImage = rasterio.open('ndviImage.tiff', 'w', driver='Gtiff',
                            width=band4.width,
                            height=band4.height,
                            count=1, crs=band4.crs,
                            transform=band4.transform,
                            dtype='float64')
    ndviImage.write(ndvi, 1)
    ndviImage.close()
    #plot ndvi
    ndvi = rasterio.open('ndviImage.tiff')
    fig = plt.figure(figsize=(18, 12))
    plot.show(ndvi, title=title)

def main():
    path1_1 = '../Clipped_NDVI/awifs_ndvi_201701_15_1_clipped.tif'
    path1_2 = '../Clipped_NDVI/awifs_ndvi_201701_15_2_clipped.tif'
    title1 = 'Barren'

    path2_1 = '../Clipped_NDVI/awifs_ndvi_201707_15_1_clipped.tif'
    path2_2 = '../Clipped_NDVI/awifs_ndvi_201707_15_2_clipped.tif'
    title2 = 'First Peak'

    path3_1 = '../Clipped_NDVI/awifs_ndvi_201808_15_1_clipped.tif'
    path3_2 = '../Clipped_NDVI/awifs_ndvi_201808_15_2_clipped.tif'
    title3 = 'Second Peak'

    generate_ndvi(path1_1, path1_2, title1)
    generate_ndvi(path2_1, path2_2, title2)
    generate_ndvi(path3_1, path3_2, title3)


if __name__ == '__main__':
    main()
