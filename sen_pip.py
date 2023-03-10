from sentinelsat import SentinelAPI
from osgeo import gdal
import xarray as xr
import s3fs
from dotenv import load_dotenv
import os
from glob import glob
import argparse
import zipfile


parser = argparse.ArgumentParser(description='sentinel ingestion pipeline')
parser.add_argument('--product_id', metavar='product_id',
                    type=str, help='enter product id', required=True)
args = parser.parse_args()
product_id = args.product_id

load_dotenv()
# Sentinel Hub credentials
apiusr = os.getenv('apiusr')
apipass = os.getenv('apipass')
api = SentinelAPI(apiusr, apipass)

# s3 credentials
acc_key = os.getenv('acc_key')
sec_key = os.getenv('sec_key')
bucket = os.getenv('bucket')
endpoint_url = os.getenv('endpoint_url')
s3 = s3fs.S3FileSystem(
    key=acc_key,
    secret=sec_key,
    client_kwargs={
        'endpoint_url': endpoint_url
    }
)

# downloading images
query_kwargs = {
    'platformname': 'Sentinel-2'
}

query_kwargs['raw'] = f'filename:{product_id}*'
pp = api.query(**query_kwargs)
# download product
api.download_all(pp)
# extract zip file to SAFE folder
with zipfile.ZipFile(f'{product_id}.zip', 'r') as zip_ref:
    zip_ref.extractall()

# resampling all the 20m bands
bands = []
bands_10 = ['B02', 'B03', 'B04', 'B08']
bands_20 = ['B05', 'B06', 'B07', 'B11', 'B12']

for item in bands_20:
    im_path = glob(f'{product_id}.SAFE/GRANULE/*/IMG_DATA/*{item}.jp2')[0]
    warped_path = im_path.replace(item, f'{item}_warped')
    ba2 = gdal.Warp(warped_path, im_path, xRes=10, yRes=10)
    bands.append(xr.open_dataarray(warped_path).rename(item))
    print(f'{item} resampled and appended')

for item in bands_10:
    im_path = glob(f'{product_id}.SAFE/GRANULE/*/IMG_DATA/*{item}.jp2')[0]
    bands.append(xr.open_dataarray(im_path).rename(item))
    print(f'{item} appended')

# create single zarr
bands = xr.merge(bands)
bands.to_zarr(f'{product_id}.zarr', mode='w')
print('zarr file created')

s3.put(f'{product_id}.zarr',
       f's3://{bucket}/{product_id}.zarr', recursive=True)
print('uploaded to s3')