
import geopandas as gpd

borough = gpd.read_file('D:/Machine Learning Projects/soil/shape file/rajanpur.shp')
borough = borough.to_crs(epsg=32642)
borough = borough.to_file('chin2.shp')
print(type(borough))
