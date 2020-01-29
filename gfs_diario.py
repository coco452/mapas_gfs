from mpl_toolkits.basemap import Basemap
import osr, gdal
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import datetime
from datetime import timedelta

today = datetime.date.today()
anio = today.year
mes = today.month
mes_str = f"{mes:02d}"
dia = today.day
start_day = f"{dia-1:02d}"
diario_str = f"{dia:02d}"
#print(type(fecha))
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
# Read the data and metadata
for i in range(4):
    print(i)
    act = today + timedelta(days=i)
    print(act)
    act_dia = act.day
    ant = today + timedelta(days=i-1)
    ant_dia = ant.day
    ant_month = ant.month
    ant_anio = ant.year
    print(ant)
    #act_dia = dia + i
    #ant_dia = act_dia -1
    act_dia = f"{act_dia:02d}"
    ant_dia = f"{ant_dia:02d}"


    anio_act = act.year
    mes_act = act.month
    mes_act_str = f"{mes_act:02d}"
    mes_ant = f"{ant_month:02d}"

    path = 'gfs.'+str(anio)+mes_str+start_day+'06.'+str(anio_act)+mes_act_str+act_dia+'12.diario'
    ds = gdal.Open(r'/home/alerta9/formularios/gfs_data/'+diario_str+'_'+mes_str+'_'+str(anio)+'/'+path+'.GTiff')
    print(path)
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
    levels = [0,0.5, 2, 6, 10, 15, 20, 30, 40, 50, 60, 70, 80,
              90, 100, 110, 130]
    norm = matplotlib.colors.BoundaryNorm(levels, 16)
    #print(xx)
    #print(yy)
    # plot the data (first layer)
    #im1 = m.pcolormesh(xx, yy, data[0,:,:].T, norm=norm ,cmap=precip_colormap)
    im1 = m.contourf(xx, yy, data[0,:,:].T, levels = levels ,norm=norm ,cmap=precip_colormap, extend = "max")
    m.colorbar(im1 , label='Precipitación [mm]')

    # annotate
    m.drawcountries()
    m.drawstates(color='grey', linewidth = 0.5)
    m.drawrivers(color='#0000ff', linewidth = 0.2)
    m.drawcoastlines(linewidth=.5)
    plt.title("Precipitación acumulada diaria - "+ant_dia+'/'+mes_ant+'/'+str(anio)+' - '+act_dia+'/'+mes_act_str+'/'+str(anio))
    plt.savefig('/home/alerta9/formularios/gfs_data/'+diario_str+'_'+mes_str+'_'+str(anio)+'/'+path+'.png',dpi=150, bbox_inches='tight', pad_inches=0)
