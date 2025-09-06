import sys
import os.path as path
two_up =  path.abspath(path.join(__file__ ,"../.."))
sys.path.append(two_up)

import tmart
import numpy as np

try:
    from Py6S import AtmosProfile
    PY6S_AVAILABLE = True
except Exception:
    PY6S_AVAILABLE = False

atm_profile = AtmosProfile.PredefinedType(AtmosProfile.MidlatitudeSummer) 
aerosol_type = 'Maritime' 
aot550 = 0.1
n_layers = 20
aerosol_scale_height = 2 
wl = 400

### DEM and reflectance ###
image_DEM = np.array([[0,0],[0,0]]) # in meters
image_reflectance = np.array([[0.00,0.00],[0.00,0.00]]) # unitless     
# image_isWater = np.zeros(image_DEM.shape) # 1 is water, 0 is land
image_isWater = np.array([[1,1],[1,1]]) 



my_atm = tmart.Atmosphere(atm_profile, aot550, aerosol_type, n_layers, aerosol_scale_height)
#atm_profile_wl, aerosol_SPF_wl, T_gaz_total = my_atm._wavelength(wl,band=None)
#print(f'total gaseous transmittance (downward and upward directions): {T_gaz_total}')

my_surface = tmart.Surface(DEM = image_DEM,
                           reflectance = image_reflectance,
                           isWater = image_isWater,
                           cell_size = 10_000)  
           
my_surface.set_background(bg_ref        = 0.0, # background reflectance
                          bg_isWater    = 1, # if is water
                          bg_elevation  = 0, # elevation of both background
                          bg_coords     = [[0,0],[10,10]]) # a line dividing the two background                                    
     
my_tmart = tmart.Tmart(Surface = my_surface, Atmosphere= my_atm, shadow=False)



sensor_coords=[51,50,130_000]


my_tmart.set_geometry(sensor_coords=sensor_coords, 
                      target_pt_direction=[170.52804413432926, 191.91873559828522],
                      sun_dir=[30.9608405674786, 323.9885587375248])



results = my_tmart.run(wl=wl, n_photon=10_000)

# Calculate reflectances using recorded photon information 
R = tmart.calc_ref(results,detail=True)
for k, v in R.items():
    print(k, '     ' , v)



my_atm_profile = my_tmart.atm_profile_wl
np.sum(my_atm_profile.ot_mie)
print(f'total gaseous transmittance (downward and upward directions): {my_tmart.T_gaz_total}')


