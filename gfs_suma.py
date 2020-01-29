from mpl_toolkits.basemap import Basemap
import osr, gdal
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import datetime
from datetime import timedelta

def convertXY(xy_source, inproj, outproj):
    # function to convert coordinates

    shape = xy_source[0,:,:].shape
    size = xy_source[0,:,:].size

    # the ct object takes and returns pairs of x,y, not 2d grids
    # so the the grid needs to be reshaped (flattened) and back.
    ct = osr.CoordinateTransformation(inproj, outproj)
    xy_target = np.array(ct.TransformPoints(xy_source.reshape(2, size).T))

    xx = xy_target[:,0].reshape(shape)
    yy = xy_target[:,1].reshape(shape)

    return xx, yy

today = datetime.date.today()
anio = today.year
mes = today.month
mes_str = "{:02d}".format(1)
dia = today.day
start_day = f"{dia-1:02d}"
diario_str = f"{dia:02d}"
act = today + timedelta(days=7)
act_dia = act.day
last_dia = "{:02d}".format(act.day)
last_mes = "{:02d}".format(act.month)


act_dia=f"{dia+7:02d}"
mes_str = "{:02d}".format(1)

#print(type(fecha))
path = 'gfs.'+str(anio)+mes_str+diario_str+'06.'+str(anio)+mes_str+diario_str+'12.suma'
#ds = gdal.Open(r'/home/alerta5/34-GFS/mapas/suma/'+path+'.GTiff')
# Read the data and metadata
ds = gdal.Open(r'/home/alerta9/formularios/gfs_data/29_01_2020/'+ path+'.GTiff')

data = ds.ReadAsArray()
gt = ds.GetGeoTransform()
proj = ds.GetProjection()

xres = gt[1]
yres = gt[5]

# get the edge coordinates and add half the resolution
# to go to center coordinates
xmin = gt[0] + xres * 0.5
xmax = gt[0] + (xres * ds.RasterXSize) - xres * 0.5
ymin = gt[3] + (yres * ds.RasterYSize) + yres * 0.5
ymax = gt[3] - yres * 0.5

ds = None

# create a grid of xy coordinates in the original projection
xy_source = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]
# Create the figure and basemap object
fig = plt.figure(figsize=(12, 6))

m = Basemap(projection='lcc', resolution='i',
            width=8E6, height=8E6, lat_1=-10,lat_2=-30,
            lat_0=-37, lon_0=-60)
m.drawparallels(np.arange(-90.,91.,10.))
m.drawmeridians(np.arange(-180.,181.,20.))
# Create the projection objects for the convertion
# original (Albers)
inproj = osr.SpatialReference()
inproj.ImportFromWkt(proj)

# Get the target projection from the basemap object
outproj = osr.SpatialReference()
outproj.ImportFromProj4(m.proj4string)

# Convert from source projection to basemap projection
xx, yy = convertXY(xy_source, inproj, outproj)
nws_precip_colors = [
    "#f9f9f9",  # 0 - 0.5 mm
    "#04e9e7",  # 0.5 - 2 mm
    "#019ff4",  # 2 - 6 mm
    "#0300f4",  # 6 - 10 mm
    "#02fd02",  # 10 - 15 mm
    "#01c501",  # 15 - 20 mm
    "#008e00",  # 20 - 30 mm
    "#fdf802",  # 30 - 40 mm
    "#e5bc00",  # 40 - 50 mm
    "#fd9500",  # 50 - 60 mm
    "#fd0000",  # 60 - 70 mm
    "#d40000",  # 70 - 80 mm
    "#bc0000",  # 80 - 90 mm
    "#f800fd",  # 90 - 100 mm
    "#9854c6",  # 100 - 110 mm
    "#0a0a0a",  # 110 - 130 mm
]
precip_colormap = matplotlib.colors.ListedColormap(nws_precip_colors)
levels = [0,1, 4, 12, 20, 30, 40, 60, 80, 100, 120, 140, 160,
          180, 200, 250, 300]
norm = matplotlib.colors.BoundaryNorm(levels, 16)
print(xx)
print(yy)
# plot the data (first layer)
im1 = m.contourf(xx, yy, data[0,:,:].T , vmin=0, vmax=300, levels=levels , cmap='rainbow' , extend = "max")
m.colorbar(im1 ,label='Precipitación [mm]')

# annotate
m.drawcountries()
m.drawrivers(color='#0000ff', linewidth = 0.2)
m.drawcoastlines()
m.drawstates(color = 'grey', linewidth =0.2)
m.readshapefile('/home/alerta9/goes/goes_data/cdp/cdp','cdp',linewidth=0.5,color='red')
plt.title("Precipitación acumulada semanal - 09/01/2020 - 16/01/2020")
plt.savefig('5.png',dpi=300)
plt.title("Precipitación acumulada semanal - "+diario_str+'/'+mes_str+'/'+str(anio)+' - '+last_dia+'/'+last_mes+'/'+str(anio))
plt.savefig('/home/alerta9/formularios/gfs_data/'+diario_str+'_'+mes_str+'_'+str(anio)+'/'+path+'.png',dpi=150, bbox_inches='tight', pad_inches=0)
#################################################################################
