#
#
# script to download the ERA5 100m winds,T2m and RSDS from the climate data store api.
#
#
#
import cdsapi


for YEAR in range(2020,2021):
    for MONTH in range(1,13):

        # firstly get the correct number of days in each month.
        if MONTH in [9,4,6,11]:
            day_array = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']
        elif MONTH in [2]:
            if YEAR in [1980,1984,1988,1992,1996,2000,2004,2008,2012,2016,2020]:
                day_array = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29']
            else:
                day_array = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28']	 
        else:
            day_array = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']   	           
     

        m = str(MONTH).zfill(2) # make sure it is 01, 02 etc
        y = str(YEAR)
        c = cdsapi.Client()
        r = c.retrieve('reanalysis-era5-single-levels',{'variable':['100m_u_component_of_wind','100m_v_component_of_wind','2m_temperature','surface_solar_radiation_downwards'],
                                                        'product_type':'reanalysis',
                                                        'year':[y],
                                                        'month':[m],
                                                        'day':day_array,
                                                        'time':['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00'],
                                                        'area' : [90,-45,29.8,40.3],# N/W/S/E 
                                                        'grid'      : "0.28/0.28",
                                                        'format':'netcdf'}) # same area as seasonal forecasts
        r.download('TEST_1hr_' +str(y) + '_' + str(m) + '_DET.nc')


