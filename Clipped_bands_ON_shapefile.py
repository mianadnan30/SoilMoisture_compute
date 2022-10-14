import os
import rasterio
import fiona
from rasterio import mask as msk
allfiles=os.listdir('D:/Machine Learning Projects/soil/tiles')
path_of_the_tiles='D:/Machine Learning Projects/soil/tiles/'
tiles_clipped='D:/Machine Learning Projects/soil/clipped'
shape_file_path='D:/Machine Learning Projects/soil/chin2.shp'

def Clipped_Raster(raster_file, shapefile, path_to_save_clipped_raster, ifile):
    print("raster_file is ", raster_file)
    with rasterio.open(raster_file) as src:
        NDVI_crs = src.crs
        with fiona.open(shapefile, "r") as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]
        out_image, out_transform = msk.mask(src, shapes, crop=True, all_touched=True)
        out_meta = src.meta
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})
    print(path_to_save_clipped_raster)
    path_to_save_clipped_raster = path_to_save_clipped_raster + "/" + "Clipped_" + ifile
    with rasterio.open(path_to_save_clipped_raster, "w", **out_meta) as dest:
        dest.write(out_image)
    return 'path_to_save_clipped_raster'



for ifile in allfiles:
    band_id=ifile[:40]
    print("band is ",band_id)
    print(ifile)
    raster_file='D:/Machine Learning Projects/soil/china_tiles/'+ifile
    # print(raster_file)
    if ifile.endswith(band_id + "_SR_B4.TIF"):
        raster_file = path_of_the_tiles + ifile
        print(raster_file)
        # print(shape_file_path+str(form_id)+"/"+str(form_id)+".shp")
        clipped = Clipped_Raster(raster_file, shape_file_path,  tiles_clipped, ifile)
    elif ifile.endswith(band_id + "_SR_B5.TIF"):
        raster_file = path_of_the_tiles + ifile
        clipped = Clipped_Raster(raster_file, shape_file_path,  tiles_clipped, ifile)
    elif ifile.endswith(band_id + "_ST_B10.TIF"):
        raster_file = path_of_the_tiles + ifile
        clipped = Clipped_Raster(raster_file, shape_file_path,  tiles_clipped, ifile)
    clipped = Clipped_Raster(raster_file, shape_file_path,  tiles_clipped, ifile)

# ///////////////////////////////////////////////////////////////////////////
# Create shape file and clip bands
# def clipped(path_of_the_tiles,clipped_file_path,Tile_id,shape_file_path,polygon,form_id):
#
#     def get_crs(path_of_the_tiles):
#         with rasterio.open(path_of_the_tiles) as src:
#             NDVI_crs = src.crs
#             print("crs is ",NDVI_crs)
#             # src.close()
#         return NDVI_crs
#     def shape_file(polygon, crs,shape_file_path):
#         poly_df = gpd.GeoDataFrame(geometry=[polygon], crs="EPSG:4326")
#         poly_df = poly_df.to_crs(crs)
#         shape_file=poly_df.to_file(shape_file_path+str(form_id))
#         print(shape_file)
#         return "shape_file"
#
#     def Clipped_Raster(raster_file,shapefile, path_to_save_clipped_raster,ifile):
#         print("raster_file is ",raster_file)
#         with rasterio.open(raster_file) as src:
#             NDVI_crs = src.crs
#             with fiona.open(shapefile, "r") as shapefile:
#                 shapes = [feature["geometry"] for feature in shapefile]
#             out_image, out_transform = msk.mask(src, shapes, crop=True, all_touched=True)
#             out_meta = src.meta
#         out_meta.update({"driver": "GTiff",
#                          "height": out_image.shape[1],
#                          "width": out_image.shape[2],
#                          "transform": out_transform})
#         # print(path_to_save_clipped_raster)
#         path_to_save_clipped_raster= path_to_save_clipped_raster+ "/" +"Clipped_"+ifile
#         with rasterio.open(path_to_save_clipped_raster, "w", **out_meta) as dest:
#             dest.write(out_image)
#         return path_to_save_clipped_raster
#
#
#     allfiles = os.listdir(path_of_the_tiles)
#     band_id = Tile_id[:-3]
#     for ifile in allfiles:
#         if ifile.endswith(band_id + "_SR_B4.TIF"):
#             NDVI_cr = get_crs(path_of_the_tiles+ifile)
#             shape_file_paths=shape_file(polygon, NDVI_cr, shape_file_path)
#             print("shape file path is",shape_file_paths)
#
#
#     for ifile in allfiles:
#         if ifile.endswith(band_id + "_SR_B4.TIF"):
#             raster_file=path_of_the_tiles+ ifile
#             # print(shape_file_path+str(form_id)+"/"+str(form_id)+".shp")
#             clipped =Clipped_Raster(raster_file, shape_file_path+"/"+str(form_id)+"/"+str(form_id)+".shp", clipped_file_path,ifile)
#         elif ifile.endswith(band_id + "_SR_B5.TIF"):
#             raster_file=path_of_the_tiles+ ifile
#             clipped =Clipped_Raster(raster_file, shape_file_path+"/"+str(form_id)+"/"+str(form_id)+".shp", clipped_file_path,ifile)
#         elif ifile.endswith(band_id + "_ST_B10.TIF"):
#             raster_file=path_of_the_tiles+ ifile
#             clipped =Clipped_Raster(raster_file,shape_file_path+"/"+str(form_id)+"/"+str(form_id)+".shp", clipped_file_path,ifile)
#
#     return "Clipped Files"
#
