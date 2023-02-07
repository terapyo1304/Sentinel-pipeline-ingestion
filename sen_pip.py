from sentinelsat import SentinelAPI
import scipy
from datetime import date
import geopandas 
import numpy as np
from matplotlib.image import imread
from PIL import Image
api=SentinelAPI('aryamanskatoch', 'Chungus-rdr2')
s_date=date(2023, 1, 11)
f_date=date.today()
query_kwargs = {
        'platformname': 'Sentinel-2',
        'producttype': 'S2MSI1C',
        'date': (s_date, f_date)}

kw=query_kwargs.copy()
kw['raw']=f'filename:S2B_MSIL1C_20230206T090039_N0509_R007_T33MYU_20230206T105859.SAFE'
pp=api.query(**kw)
api.download_all(pp)
file=''
bird= imread('/Users/indukatoch/Desktop/Sentinel-pipeline-ingestion-1/IMG_6588.jpeg')
print(bird.size, bird.shape, bird.ndim)



print("aryaman")


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
    img2.save(newName)