from pystac_client import Client
import os
import boto3
band_local_path='D:/Machine Learning Projects/soil/tiles/'
timeRange = '2021-01-01/2021-03-28'
lat = 29.078468
lon = 70.327666
LandsatSTAC = Client.open("https://landsatlook.usgs.gov/stac-server", headers=[])
def CreateSquarePolygone(lon,lat,timeRange):

    def BuildSquare(lon, lat, delta):
        c1 = [lon + delta, lat + delta]
        c2 = [lon + delta, lat - delta]
        c3 = [lon - delta, lat - delta]
        c4 = [lon - delta, lat + delta]
        geometry = {"type": "Polygon", "coordinates": [[ c1, c2, c3, c4, c1 ]]}
        return geometry
# Create square shape file from a single point
    geometry = BuildSquare(	lon,lat, 0.04)
# Check the tiles available in the given timerange
    LandsatSearch = LandsatSTAC.search (
        intersects =geometry,
        datetime = timeRange,
        query =  ['eo:cloud_cover95'],
        collections = ["landsat-c2l2-sr"] )
    Landsat_items = [i.to_dict() for i in LandsatSearch.get_items()]
    return Landsat_items
# Call the function to find the tiles
Landsat_items=CreateSquarePolygone(lon,lat,timeRange)
print(f"{len(Landsat_items)} Landsat scenes fetched")
# //////////////////////////////////////////////////////////////////////////////////////////
def get_tile_paths(Landsat_items):
#     Get year
    date_string = Landsat_items['properties']['datetime']
    year = date_string[0:4]
    # Get wrs_row and wrs_path
    wrs_path = Landsat_items['properties']['landsat:wrs_path']
    wrs_row = Landsat_items['properties']['landsat:wrs_row']
    epsg=Landsat_items['properties']['proj:epsg']
    # create id's'
    id2 = Landsat_items['id']
    id1 = id2[:-3]
    # create tile path
    temp_path = "collection02/level-2/standard/oli-tirs"
    tile_path = temp_path + "/" + year + "/" + wrs_path + "/" + wrs_row + "/" + id1 + "/" + id1
    return tile_path,epsg
# tilpath,a=get_tile_paths(j)
# print(tilpath,a)
# ////////////////////////////////////////////////////////////////////////////////////////////

def tiles_down(Landsat_items,band_local_path):
    for i in Landsat_items:
        if i['properties']['platform'] == "LANDSAT_8" and i['properties']['proj:epsg'] == 32642:
            tile_id = i['id']
            id1 = tile_id[:-3]
            # Get tilePath
            tile_paths,epsg=get_tile_paths(i)
            s3_client = boto3.client('s3')
            for i in range(4, 15):
                if i == 4:
                    band = '_SR_B4.TIF'
                    band_name = id1 + '_SR_B4.TIF'
                    s3_source= tile_paths + band
                    print("s3_source",s3_source)
                    response = s3_client.get_object(Bucket='usgs-landsat',
                                                    Key=s3_source,
                                                    RequestPayer='requester')
                    response_content = response['Body'].read()
                    print(response_content)
                    with open(band_local_path + band_name, 'wb') as file:
                        file.write(response_content)
                elif i == 5:
                    print(5)
                    band_name =  id1 + '_SR_B5.TIF'
                    band = '_SR_B5.TIF'
                    s3_source = tile_paths + band
                    response = s3_client.get_object(Bucket='usgs-landsat',
                                                    Key=s3_source,
                                                    RequestPayer='requester')
                    response_content = response['Body'].read()
                    print(response_content)
                    with open(band_local_path + band_name, 'wb') as file:
                        file.write(response_content)
                elif i == 10:
                    band_name = id1 + '_ST_B10.TIF'
                    band = '_ST_B10.TIF'
                    s3_source = tile_paths + band
                    response = s3_client.get_object(Bucket='usgs-landsat',
                                                    Key=s3_source ,
                                                    RequestPayer='requester')
                    response_content = response['Body'].read()
                    print(response_content)
                    with open(band_local_path + band_name, 'wb') as file:
                        file.write(response_content)
    return "Tiles Downloaded"
# td=tiles_down(Landsat_items,band_local_path)
# print(td)
# //////////////////////////////////////////////////////////////////////////////////////////////////////