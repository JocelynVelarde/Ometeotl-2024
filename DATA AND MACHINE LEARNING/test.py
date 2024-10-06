import proplot as plot
import xarray as xr

dem = xr.open_rasterio('https://download.osgeo.org/geotiff/samples/pci_eg/latlong.tif')
dem = dem[0]

# Define extents
lat_min = dem.y.min()
lat_max = dem.y.max()
lon_min = dem.x.min()
lon_max = dem.x.max()

#Starting the plotting
fig, axs = plot.subplots(proj=('cyl'))

#format the plot
axs.format(
    lonlim=(lon_min, lon_max), latlim=(lat_min, lat_max),
    land=False, labels=True, innerborders=False
)

#Plot
m = axs.pcolorfast(dem, cmap='batlow')
cbar = fig.colorbar(m, loc='b', label='whatever') #Adding colorbar with label

#Saving the Figure
fig.savefig(r'geotiff.png')  
