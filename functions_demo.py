import energy_model_functions
import matplotlib.pyplot as plt
import numpy as np


#
#
# SOLAR PV MODEL EXAMPLE
#
#
#
t2m_data,country_mask = energy_model_functions.load_country_weather_data('France','/storage/silver/S2S4E/energymet/ERA5/native_grid_hourly/','ERA5_1hr_2020_01_DET.nc','t2m')

print(np.shape(t2m_data))

plt.imshow(country_mask)

plt.show()

plt.imshow(t2m_data[0,:,:])

plt.show()

ssrd_data,country_mask = energy_model_functions.load_country_weather_data('France','/storage/silver/S2S4E/energymet/ERA5/RSDS/native_grid_hourly/','ERA5_1hr_RSDS_2020_01_DET.nc','ssrd')

plt.imshow(ssrd_data[0,:,:])

plt.show()

plt.imshow(ssrd_data[12,:,:])

plt.show()


solar_pv_cf = solar_PV_model(t2m_data,ssrd_data)

plt.plot(solar_pv_cf)

plt.show()


#
#
# DEMAND MODEL EXAMPLE
#
#
#

t2m_data,country_mask = energy_model_functions.load_country_weather_data('France','/storage/silver/S2S4E/energymet/ERA5/native_grid_hourly/','ERA5_1hr_2020_01_DET.nc','t2m')

hdd, cdd = energy_model_functions.calc_hdd_cdd(t2m_data)

demand_timeseries = energy_model_functions.calc_national_wd_demand_2017(hdd,cdd,filestr_reg_coefficients,COUNTRY)



#
#
#
# WIND POWER EXAMPLE
#
#
#

speed100m_data,country_mask = energy_model_functions.load_100mwindspeed_data('/storage/silver/S2S4E/energymet/ERA5/native_grid_hourly/','ERA5_1hr_2020_01_DET.nc','u100m','v100m')
