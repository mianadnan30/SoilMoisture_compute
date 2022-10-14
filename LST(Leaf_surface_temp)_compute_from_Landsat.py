import numpy as np
import numpy as np
import rasterio
import os
path_of_the_tiles='D:/Machine Learning Projects/soil/tiles/'
shape_file_path='D:/Machine Learning Projects/soil/chin2.shp'
tiles_clipped_path='D:/Machine Learning Projects/soil/clipped/'
allfiles=os.listdir('D:/Machine Learning Projects/soil/clipped')
path_of_the_LST_tiles='D:/Machine Learning Projects/soil/lst/'

def lst_computes(tiles_clipped_path,Tile_id ):

    band_id = Tile_id
    for ifile in allfiles:

        if ifile.endswith(band_id+"_SR_B4.TIF"):
            print(ifile)
            print("band is ", band_id)
            path = tiles_clipped_path + ifile
            print("path is of band 4 ",path)
            band4 = rasterio.open(path)
            red = band4.read(1).astype('float64')
            print("band4",band4)
        elif ifile.endswith(band_id+"_SR_B5.TIF"):
            print("band is ", band_id)
            path = tiles_clipped_path + ifile
            print("band 5 path is",path)
            band5 = rasterio.open(path)
            nir = band5.read(1).astype('float64')
            print(nir,"nir")
        elif ifile.endswith(band_id+"_ST_B10.TIF"):
            path = tiles_clipped_path  + ifile
    #         # print(path)
            band10 = rasterio.open(path)
            tempImage10 = band10.read(1).astype('float64')
            print(tempImage10)
    TOA=((tempImage10)*0.0003342)+0.1
    BT = (1321.0789 / np.log((774.8853 / TOA) + 1)) - 273.15
    ndvi=np.where(
        (nir+red)==0.,
        0,
        (nir-red)/(nir+red))

    max_ndvi=np.max(ndvi)
    print('max ndvi is',max_ndvi)
    min_ndvi=np.min(ndvi)
    print('min ndvi is', min_ndvi)

    PV= (ndvi -min_ndvi)/(max_ndvi-min_ndvi)**2
    E = 0.004 * PV + 0.986
    LST=(BT / (1 + (0.00115 * BT / 1.4388) *  np.log(E)))

    x = LST[~np.isnan(LST)]

    LSTavg = np.average(x)
    print("LSt", LSTavg)
    y = ndvi[~np.isnan(LST)]

    ndviavg = np.average(y)
    print("Ndvi ",ndviavg)
    print("min ", np.average(min_ndvi))
    print("Max ", np.average(max_ndvi))

    # print(LST)

    image=rasterio.open(path_of_the_LST_tiles+Tile_id+"_LST.TIF",'w',driver='Gtiff',
                        width=LST.shape[0],
                        height=LST.shape[0],
                       count=1,
                       crs=band5.crs,
                       transform=band5.transform,
                       dtype='float64')
    image.write(LST,1)
    image.close()
    return "lst create"

for ifile in allfiles:
    # print(ifile)
    band_id = ifile[:48]
    print('band id is ',band_id)
    lst=lst_computes(tiles_clipped_path, band_id)
    print(lst)
