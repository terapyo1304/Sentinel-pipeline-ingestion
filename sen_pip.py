
from aioitertools import product
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
product_id='S2A_MSIL1C_20230218T085021_N0509_R107_T34NCF_20230218T123025'
kw=query_kwargs.copy()
kw['raw']=f'filename:{product_id}*'
pp=api.query(**kw)
print(pp)
api.download_all(pp)


#resampling all the 20m bands
bands=[]
bands_10=['B02','B03','B04','B08']
bands_20=['B05','B06','B07','B11','B12']
for item in bands_20:
        im_path=glob(f'{product_id}.SAFE/GRANULE/*/IMG_DATA/*{item}.jp2')[0]
        warped_path=im_path.replace(item,f'{item}_warped')
        ba2=gdal.Warp(warped_path,im_path,xRes=10,yRes=10)
        bands.append(xr.open_dataarray(warped_path).rename(item))
        

for item in bands_10:
        im_path=glob(f'{product_id}.SAFE/GRANULE/*/IMG_DATA/*{item}.jp2')[0]
        bands.append(xr.open_dataarray(im_path).rename(item))

bands=xr.merge(bands)
bands.to_zarr(f'{product_id}.zarr',mode='w')

s3 = s3fs.S3FileSystem(
      key=acc_key,
      secret=sec_key,
      client_kwargs={
         'endpoint_url': 'http://cyclops.ap-south-1.linodeobjects.com/'
      }
   )

s3.put(f'{product_id}.zarr', f's3://cyclops/{product_id}.zarr' , recursive=True)
        

                     

