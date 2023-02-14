from sentinelsat import SentinelAPI
import scipy.misc as misc #not working
import scipy.ndimage
from datetime import date
import imageio as iio
import geopandas 
import numpy as np
import matplotlib.image as mpimg
from PIL import Image
from osgeo import gdal
import pandas as pd
import xarray
import re
api=SentinelAPI('aryamanskatoch', 'Chungus-rdr2')
s_date=date(2023, 1, 11)
f_date=date.today()
query_kwargs = {
        'platformname': 'Sentinel-2',
        'producttype': 'S2MSI1C',
        'date': (s_date, f_date)}

kw=query_kwargs.copy()
kw['raw']=f'filename:S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE'
'''pp=api.query(**kw)
api.download_all(pp)'''
file=''
bird= gdal.Open('/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B05.jp2')
bird_array= mpimg.imread('/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B05.jp2')
#print(bird.size, bird.shape, bird.ndim)
print(bird_array)
ba2=gdal.Warp('/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B05_resampled.jp2',bird,xRes=10,yRes=10)
ba2=iio.imread('/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B05_resampled.jp2')
print('resampled:',ba2)





#print("aryaman")

#resampling all the 20m bands
'''np_array=[]
bands=['/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B02.jp2','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B03.jp2','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B04.jp2','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B05.jp2','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B06.jp2','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B07.jp2','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B08.jp2','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B09.jp2','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B10.jp2','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B11.jp2','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B12.jp2']
for item in bands:
    if item=='/w*B05/w*' or item=='/w*B06/w*' or item=='/w*B07/w*' or item=='/w*B11/w*' or item=='/w*B12/w*':
        bird= gdal.Open(item)
        bird_array= iio.imread(item)
        #print(bird.size, bird.shape, bird.ndim)
        print(bird_array)
        ba2=gdal.Warp(item,bird,xRes=2,yRes=2)
        ba2=iio.imread(item)
        #print('resampled:',ba2)
        np_array.append(ba2)
    else:
        bird= gdal.Open(item)
        bird_array= iio.imread(item)
        np_array.append(bird_array)'''
    
        
#convert to dask        
'''bands_dask=dask.array.from_array(np.load(np_array, mmap_mode='r')
#convert to xarray
#convert numpy array to dataset
bands_ds = bands.to_dataset(name='bands') #convert numpy array to dataset
#convert to zarr
bands_zarr = bands_ds.to_zarr('/home/indukatoch/Sentinel-pipeline-ingestion/bands.zarr')'''
                     

'''
def resizelayer(old):
    rows,cols=old.shape
    #move old points
    rNew=2*rows-1
    cNew=2*cols-1
    new=np.zeros((rNew,cNew))
    new[0:rNew:2, 0:cNew:2]=old[0:rows,0:cols]

    #produce vertical values
    new[1:rNew:2,:]=(new[0:rNew-1:2,:]+new[2:rNew:2,:])/2

    #produce horizontal values
    new[:,1:cNew:2]=(new[:,0:cNew-1:2]+new[:,2:cNew:2])/2
    return new
print(resizelayer(bird))

rows,cols,layers=bird.shape
new=np.zeros((2*rows-1,2*cols-1,layers))
print('original dimensions=',bird.shape)
for layer in range(3):
    new[:,:,layer]=resizelayer(bird[:,:,layer])

    new=new.astype(np.uint8)
    print("new dimensions=",new.shape)

    img2=Image.formarray(new) #new image formed
    newName="big-"+bird
    img2.save(newName)'''