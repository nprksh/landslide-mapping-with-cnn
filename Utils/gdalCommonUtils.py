import numpy as np
import csv
import sys
import os
from osgeo import gdal, gdalnumeric


NP2GDAL_CONVERSION = {
  "uint8": gdal.GDT_Byte,
  "int8": gdal.GDT_Byte,
  "uint16": gdal.GDT_UInt16 ,
  "int16": gdal.GDT_Int16,
  "uint32": gdal.GDT_UInt32,
  "int32": gdal.GDT_Int32,
  "float32": gdal.GDT_Float32,
  "float64": gdal.GDT_Float64,
#   "complex64": gdal.GDT_Int16,
#   "complex128": gdal.GDT_Int16,
}


def readGDAL2numpy(rasterPath, return_geoInformation = False):
    try:
        ds = gdal.Open(rasterPath)
    except RuntimeError:
        print('Unable to open input file')
        sys.exit(1)
    
    data = gdalnumeric.LoadFile(rasterPath, False)
    noDataVal = ds.GetRasterBand(1).GetNoDataValue()
    try:
        if data.dtype in ['float16', 'float32', 'float64'] and noDataVal is not None:
            data[data == noDataVal] = np.NaN
    except:
        print("Issue in no data value")
    
    if len(data.shape) == 3:
        data = np.transpose(data , (1, 2, 0))
        
    if return_geoInformation == False:
        return data
    else:
        geoTransform = ds.GetGeoTransform()
        projection = ds.GetProjection()    
        return data, geoTransform, projection



def writeNumpyArr2Geotiff(outputPath, data, geoTransform = None, projection = None, GDAL_dtype = None, noDataValue = None, colorTable = None):
    nscn, npix = data.shape

    if GDAL_dtype is None:
        GDAL_dtype = NP2GDAL_CONVERSION[data.dtype.name]
    
    if np.isnan(data).any() and noDataValue is not None:
        print('Here1')
        data[np.isnan(data)] = noDataValue
    
    ds_new = gdal.GetDriverByName('GTiff').Create(outputPath, npix, nscn, 1, GDAL_dtype)
    
    if geoTransform != None:
        ds_new.SetGeoTransform(geoTransform)
        
    if projection != None:
        ds_new.SetProjection(projection)    
    
    outBand = ds_new.GetRasterBand(1)
    outBand.WriteArray(data)
    
    if noDataValue != None:
        ds_new.GetRasterBand(1).SetNoDataValue(noDataValue)

    if colorTable != None:
        ds_new.GetRasterBand(1).SetRasterColorTable(colorTable)

    # Close dataset
    ds_new.FlushCache()
    ds_new = None
    outBand = None



def newGeoTransform(geoTransform, maskBounds):
    newGeoTransform = (geoTransform[0]+ maskBounds['xMin'] * geoTransform[1],
                   geoTransform[1],
                   geoTransform[2],
                   geoTransform[3] + maskBounds['yMin'] * geoTransform[5],
                   geoTransform[4],
                   geoTransform[5])  
    return newGeoTransform



def bbox(img):
    scn = np.any(img, axis=1)
    pix = np.any(img, axis=0)
    scnMin, scnMax = np.where(scn)[0][[0, -1]]
    pixMin, pixMax = np.where(pix)[0][[0, -1]]
    return [scnMin, scnMax, pixMin, pixMax]



def getBoundingBox(rasterPath, returnBinaryMask = False):
    image, geoT, proj = readGDAL2numpy(rasterPath, return_geoInformation = True)
    
    yMin, yMax, xMin, xMax = bbox(image)
        
    if returnBinaryMask:
        maskImage = image[yMin : yMax, xMin : xMax]
        maskGeoT  = newGeoTransform(geoT, {'xMin' : xMin, 'yMin' : yMin})
        return [yMin, yMax, xMin, xMax], maskImage, maskGeoT, proj
    else:
        return [yMin, yMax, xMin, xMax]