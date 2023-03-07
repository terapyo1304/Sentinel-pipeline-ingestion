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
from glob import glob
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
        'platformname': 'Sentinel-2'
               }

kw=query_kwargs.copy()
kw['raw']=f'filename:S2A_MSIL1C_20230218T085021_N0509_R107_T34NCF_20230218T123025*'
pp=api.query(**kw)
print(pp)
api.download_all(pp)


#resampling all the 20m bands
bands=[]
bands_10=['*/B02/*','*/B03/*','*/B04/*','*/B08/*']
bands_20=['*/B05/*','*/B06/*','*/B07/*','*/B11/*','*/B12/*']
for item in bands_20:
        im_path='S2A_MSIL1C_20230218T085021_N0509_R107_T34NCF_20230218T123025.SAFE/GRANULE/*/IMG_DATA/*.jp2'
        if item in glob(im_path):
                bird= gdal.Open(im_path)
                ba2=gdal.Warp(im_path,bird,xRes=10,yRes=10)
                ba2_ar=iio.imread(im_path)
                bands.append(xr.open_dataarray(ba2_ar))

for item in bands_10:
        im_path='S2A_MSIL1C_20230218T085021_N0509_R107_T34NCF_20230218T123025.SAFE/GRANULE/*/IMG_DATA/*.jp2'
        if item in glob(im_path):
                bird= gdal.Open(im_path)
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
        

                     

