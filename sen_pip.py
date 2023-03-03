import dotenv
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
import xarray as xr
import re
import s3fs
from dotenv import load_dotenv
import os
import logging
import boto3
from botocore.exceptions import ClientError
load_dotenv()
apiusr=os.getenv('apiusr')
apipass=os.getenv('apipass')
acc_key=os.getenv('acc_key')
sec_key=os.getenv('sec_key')
bucket=os.getenv('bucket')
api=SentinelAPI(apiusr,apipass)
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




#print("aryaman")

#resampling all the 20m bands
bands=[]
bands_10=['/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B02','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B03','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B04','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B08',]
bands_20=['/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B05','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B06','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B07','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B11','/home/indukatoch/Sentinel-pipeline-ingestion/S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE/GRANULE/L1C_T33MYU_A030921_20230206T091138/IMG_DATA/T33MYU_20230206T090039_B12']
for item in bands_20:
    
        itname=item+'.jp2'
        bird= gdal.Open(itname)
        
        dest=item+'_resampled.jp2'
        ba2=gdal.Warp(dest,bird,xRes=10,yRes=10)
        ba2_ar=iio.imread(dest)
        
        bands.append(xr.open_dataarray(ba2_ar))

for item in bands_10:
        itname=item+'.jp2'
        bird= gdal.Open(itname)
        bands.append(xr.open_dataarray(bird))

bands=xr.merge(bands)
bands.to_zarr('/home/indukatoch/Sentinel-pipeline-ingestion/bands.zarr')

s3 = s3fs.S3FileSystem(
      key=acc_key,
      secret=sec_key,
      client_kwargs={
         'endpoint_url': 'http://cyclops.ap-south-1.linodeobjects.com/'
      }
   )


def upload_data(filepath, file_name):
    s3 = s3fs.S3FileSystem()
    s3_path = f"cyclops/{img.zarr}"
    s3.put(filepath, s3_path, recursive=True)
        

                     

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