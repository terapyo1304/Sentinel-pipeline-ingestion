# Sentinel-pipeline-ingestion
Automate Sentinel 2 Ingestion via GitHub Actions.

OBJECTIVE: 
  Automate Sentinel 2 ingestion via GitHub Actions and Python.

STEPS INVOLVED:
  1. Download data from ESA Copernicus based on Sentinel product ID.
  2. Resample 20m bands to 10m.
  3. Merge all 10m bands into single zarr.
  4. Upload zarr to S3.
  5. Automate entire process in GitHub Actions.

LIBRARIES USED:
  1. sentinelsat
  2. gdal
  3. xarray
  4. s3fs
  5. dotenv
  6. os
  7. glob
  8. argparse
  9. zipfile

WORKING:
  Enter the product ID in action workflows.
  The contents will be downloaded using SentinelAPI.
  The 20m bands will be resampled to 10m bands using gdal's warp function.
  The original 10m and resampled 10m bands are appended to a unified list bands.
  Added the credentials to .env file and added the same to the .gitignore file.
  Mapped the .env variables to the working file using glob function from glob library.
  Merged the contents of the list bands using xarray's merge function.
  Finally converted the entire list into a single zarr and uploaded to S3.
  

  
