#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 15:45:23 2025

@author: aparies
"""


import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import cmocean
import numpy as np


# --- ouverture du fichier ---
chemin_KINOMED = "/home/aparies/Bureau/KINOMED/DATA_prepro/CROCO_FILES/croco_ini_mercator_Y2019M01.nc"
#chemin_KINOMED = "/home/aparies/Bureau/script_visualisation/KINOMED_DATA/simu_janv2019_noland_rivier_new_bry/croco_avg.nc"
chemin_grd = "/home/aparies/Bureau/KINOMED/DATA_prepro/CROCO_FILES/croco_grd.nc"
ds_KINOMED = xr.open_dataset(chemin_KINOMED)
ds_grd = xr.open_dataset(chemin_grd)

# --- variables ---
lon = ds_grd['lon_rho']    # 2D
lat = ds_grd['lat_rho']    # 2D
temp = ds_KINOMED['temp'].isel(time=0, s_rho=39)
temp = temp.where(temp != 0, np.nan)

time = pd.to_datetime(ds_KINOMED['time'].values[0])

#temp = temp.where(temp != 0, np.nan)

t_min = temp.min().values
t_max = temp.max().values



# --- projection mercator ---
proj = ccrs.Mercator()

fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': proj})

# plot pcolormesh sur coordonnées 2D
pcm = ax.pcolormesh(
    lon, lat, temp,
    transform=ccrs.PlateCarree(),
    shading='auto',
    cmap='jet',
    vmin=t_min,
    vmax=t_max
)

# côtes et décor
ax.coastlines(resolution='10m', color='black')
ax.add_feature(cfeature.LAND, facecolor='white', zorder=2)
ax.add_feature(cfeature.BORDERS, linewidth=0.5)
gl = ax.gridlines(
    draw_labels=True,
    dms=True,
    x_inline=False,
    y_inline=False,
    linestyle='--',
    linewidth=0.5,
    color='gray'
)


# limites de la carte (optionnel : domaine entier du modèle)
ax.set_extent([lon.min(), lon.max(), lat.min(), lat.max()], crs=ccrs.PlateCarree())

# colorbar
cb = plt.colorbar(pcm, ax=ax, orientation='vertical', shrink=0.5, pad=0.06)
cb.set_label("Température (°C)")

#plt.title(f"GLAZUR — Température à {float(ds_GLAZUR['deptht'].isel(deptht=0))} m \n {time}")

plt.title(f"KINOMED — SST — {time}")
plt.savefig("/home/aparies/Bureau/script_visualisation/figure/KINOMED_SST.png", dpi=300, bbox_inches="tight")

plt.show()


