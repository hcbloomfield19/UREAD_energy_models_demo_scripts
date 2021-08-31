import numpy as np
import cartopy.io.shapereader as shpreader
from netCDF4 import Dataset
import shapely.geometry


def load_country_weather_data(COUNTRY,data_dir,filename,nc_key):

    """
    This function takes the ERA5 reanalysis data, loads it and applied a 
    country mask (ready for conversion to energy) it then returns
    the array (of original size) with all irrelvelant gridpoints 
    set to zeros.

    You will need the shpreader.natural_earth data downloaded 
    to find the shapefiles.

    Args:
        COUNTRY (str): This must be a name of a country (or set of) e.g. 
            'United Kingdom','France','Czech Republic'

        data_dir (str): The parth for where the data is stored.
            e.g '/home/users/zd907959/'

        filename (str): The filename of a .netcdf file
            e.g. 'ERA5_1979_01.nc'

        nc_key (str): The string you need to load the .nc data 
            e.g. 't2m','rsds'

    Returns:

        country_masked_data (array): Country-masked weather data, dimensions 
            [time,lat,lon] where there are 0's in locations where the data is 
            not within the country border.

        MASK_MATRIX_RESHAPE (array): Dimensions [lat,lon] where there are 1's if 
           the data is within a country border and zeros if data is outside a 
           country border. 

    """


    # first loop through the countries and extract the appropraite shapefile
    countries_shp = shpreader.natural_earth(resolution='10m',category='cultural',
                                            name='admin_0_countries')
    country_shapely = []
    for country in shpreader.Reader(countries_shp).records():
        if country.attributes['NAME_LONG'] == COUNTRY:
            print('Found country')
            country_shapely.append(country.geometry)

    # load in the data you wish to mask
    file_str = data_dir + filename
    dataset = Dataset(file_str,mode='r')
    lons = dataset.variables['longitude'][:]
    lats = dataset.variables['latitude'][:]
    data = dataset.variables[nc_key][:] # data in shape [time,lat,lon]
    dataset.close()

    # get data in appropriate units for models
    if nc_key == 't2m':
        data = data-273.15 # convert to Kelvin from Celsius
    if nc_key == 'ssrd':
        data = data/3600. # convert Jh-1m-2 to Wm-2

    LONS, LATS = np.meshgrid(lons,lats) # make grids of the lat and lon data
    x, y = LONS.flatten(), LATS.flatten() # flatten these to make it easier to 
    #loop over.
    points = np.vstack((x,y)).T
    MASK_MATRIX = np.zeros((len(x),1))
    # loop through all the lat/lon combinations to get the masked points
    for i in range(0,len(x)):
        my_point = shapely.geometry.Point(x[i],y[i]) 
        if country_shapely[0].contains(my_point) == True: 
            MASK_MATRIX[i,0] = 1.0 # creates 1s and 0s where the country is
    
    MASK_MATRIX_RESHAPE = np.reshape(MASK_MATRIX,(len(lats),len(lons)))

    # now apply the mask to the data that has been loaded in:

    country_masked_data = data*MASK_MATRIX_RESHAPE
                                     


    return(country_masked_data,MASK_MATRIX_RESHAPE)


def solar_PV_model(country_masked_data_T2m,country_masked_data_ssrd,country_mask):

    """

    This function takes in arrays of country_masked 2m temperature (celsius)
    and surface solar irradiance (Wm-2) and converts this into a time series
    of solar power capacity factor using the method from Bloomfield et al.,
    (2020) https://doi.org/10.1002/met.1858

    Args:

        country_masked_data_T2m (array): array of 2m temperatures, Dimensions 
            [time, lat,lon] or [lat,lon] in units of celsius.
        country_masked_data_ssrd (array): array of surface solar irradiance, 
            Dimensions [time, lat,lon] or [lat,lon]in units of Wm-2.
        country_mask (array): dimensions [lat,lon] with 1's within a country 
            border and 0 outside of it. 
    Returns:

        spatial_mean_solar_cf (array): Dimesions [time], Timeseries of solar 
            power capacity factor, varying between 0 and 1.


    """
   # reference values, see Evans and Florschuetz, (1977)
    T_ref = 25. 
    eff_ref = 0.9 #adapted based on Bett and Thornton (2016)
    beta_ref = 0.0042
    G_ref = 1000.
 
    rel_efficiency_of_pannel = eff_ref*(1 - beta_ref*(country_masked_data_T2m - T_ref))
    capacity_factor_of_pannel = np.nan_to_num(rel_efficiency_of_pannel*
                                              (country_masked_data_ssrd/G_ref)) 


    spatial_mean_solar_cf = np.zeros([len(capacity_factor_of_pannel)])
    for i in range(0,len(capacity_factor_of_pannel)):
        spatial_mean_solar_cf[i] = np.average(capacity_factor_of_pannel[i,:,:],
                                        weights=country_mask)

    return(spatial_mean_solar_cf)


