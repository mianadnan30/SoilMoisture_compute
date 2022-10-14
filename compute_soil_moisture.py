# Convert lst
import pandas as pd
from osgeo import gdal
import time
import numpy as np
import math
# from pylandtemp import split_window
import datetime
# utc_offset = time.localtime().tm_gmtoff
import  os
import rasterio



# Computer Soil moisture


def Get_Soil_Moisture(fpath):


    # Define global variables
    tmin_thres =0.5
    tmax_thres =100
    time_period = 3600
    albedo = None
    surf_emis =1.0
    lon=0
    lat=0
    atm_trans =0.7
    atm_emis =0.8
    rn =None
    longitude_manual = ''
    latitude_manual = ''
    h = None  # sensible heat flux
    le = None  # latent heat flux
    g = None  # ground heat flux
    ef = None  # evaporative fraction
    water = None  # amount of water

    sb_const = 5.6704*10**(-8) # Stefan Bolzmann constant
    sw_exo = 1361.5 # exo-atmospheric short wave radiation
    def get_sol_elev_ang():

      utc_offset = time.localtime().tm_gmtoff
      if  longitude_manual == '' and latitude_manual == '':
          #get day of the year, hour and minute from the datetime format
          date = datetime.datetime.now().timetuple()
          # print('date', date)
          hour = date[3]
          minute = date[4]
          # Check your timezone to add the offset
          hour_minute = (hour + minute / 60) - utc_offset
          day_of_year = date[7]

          g = (360 / 365.25) * (day_of_year + hour_minute / 24)
          g_radians = math.radians(g)
          declination = (0.396372 - 22.91327 * math.cos(g_radians) + 4.02543 *
                          math.sin(g_radians) - 0.387205 * math.cos(2 * g_radians)
                          + 0.051967 * math.sin(2 * g_radians) - 0.154527 *
                          math.cos(3 * g_radians) + 0.084798 * math.sin(3 * g_radians))

          time_correction = (0.004297 + 0.107029 * math.cos(g_radians) - 1.837877 *
                              math.sin(g_radians) - 0.837378 * math.cos(2 * g_radians) -
                              2.340475 * math.sin(2 * g_radians))

          SHA = (day_of_year - 12) * 15 + lon + time_correction

          if (SHA > 180):
              SHA = SHA - 360
          elif (SHA < -180):
              SHA = SHA + 360
          else:
              SHA = SHA
          lat_radians = math.radians(lat)
          d_radians = math.radians(declination)
          SHA_radians = math.radians(SHA)

          SZA_radians = math.acos(
                  math.sin(lat_radians) * math.sin(d_radians) + math.cos(lat_radians)
                  * math.cos(d_radians) * math.cos(SHA_radians))

          SZA = math.degrees(SZA_radians)

          SEA = 90 - SZA

          return SEA
    def read_lst_img(fpath , na_val=None):
        utc_offset = time.localtime().tm_gmtoff
        import numpy as np

    # oPEN THE RATSER BAND
        new_raster = gdal.Open(fpath,gdal.GA_ReadOnly)
        lst = new_raster.GetRasterBand(1).ReadAsArray()
        # print(lst)
        prj = new_raster.GetProjection()
        geo = new_raster.GetGeoTransform()
        lon = float(geo[0])
        lat = float(geo[3])
        # set all zeros to NaN
        lst[lst == 0.0] = na_val
        # defines tmin and tmax (minimum and maximum temperatures)
        tmin  = np.percentile(lst[~np.isnan(lst)],float(tmin_thres))
        tmax=np.percentile(lst[~np.isnan(lst)],float(tmax_thres))
        # air temperature is given with minimum temperature tmin is taken as air temperature
        air_temp= tmin
        # determines surface albedo from  from land surface temperatures and minimum and maximum temperatures
        albedo = abs(0.05 + ((lst-float(tmin))/(float(tmax)-float(tmin))) * 0.2)
        # determines short-wave irradiance
        sw_irr = sw_exo * float(atm_trans) * np.sin(np.deg2rad(get_sol_elev_ang()))
        # determines the evaporative fraction
        ef = (float(tmax)-lst)/(float(tmax)-float(tmin))
        if np.isnan(np.sum(ef)):
          pass
        else:
          ef[ef >= 1.0] = 1.0
          ef[ef <= 0.0] = 0.0
        # calculates net radiation (rn)
        # print("ef is ",ef)
        rn = ((1-albedo) * float(sw_irr) +
                        float(surf_emis) * float(atm_emis) *
                        sb_const * (air_temp**4) -
                        float(surf_emis) * sb_const *
                        (lst**4))
        # print(rn)
        # determines the ground heat flux (g)
        g = rn * (0.05 + ((lst-float(tmin))/  (float(tmax)-float(tmin))) * 0.4)
        if np.isnan(np.sum(g)):
          pass
        else:
          g[g > 1.0] = 0.45
          g[g < 0.0] = 0.05
        # determines latent heat flux (le) and sensible heat flux (h) according to evaporative fraction (ef)
        le = (rn - g) * ef
        h = (rn -g) - le
        water = ((le*float(time_period)/1000000)/
                          (2.501-0.002361*(float(air_temp)-273.15)))
        # print(time_period)
        # print(air_temp)
        return water, ef

    # call the function
    water,ef = read_lst_img(fpath , na_val=None)
    # Equation to find the soil moisture
    soil_moisture=(2.7182**((ef-1.0)/0.42))*100
    # print("soil moisture is ha",soil_moisture)
    import numpy as np
    x = soil_moisture[~np.isnan(soil_moisture)]
    arr = x
    avg = np.average(arr)
    # print("soil moisture is ",avg)
    return avg
