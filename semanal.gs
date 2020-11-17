function main( args )

base= 'nomads.ncep.noaa.gov/dods'
*base= 'nomads6.ncdc.noaa.gov:9090/dods'
*base= 'nomad5.ncep.noaa.gov:9090/dods/nomad1-raid1'
*base= 'nomad3.ncep.noaa.gov:9090/dods'

date= subwrd( args, 1 )
hour= subwrd( args, 2 )
valid= subwrd( args, 3 )

year= substr( date, 1, 4 )
mon= substr( date, 6, 2 )
day= substr( date, 9, 2 )
date= year mon day
hour= substr( hour, 1, 2 )

offs= valid / 3
if ( valid < 100 ); if ( valid < 10 ); valid= '0' valid; endif; valid= '0' valid; endif

'reinit'
'set display color white'
'c'

'set rgb 16 128 128 128'
'set rgb 17 64 64 64'

'set rgb 40 10 10 10'
'set rgb 41 253 0 0'
'set rgb 42 232 70 0'
'set rgb 43 232 101 0'
'set rgb 44 253 149 0'
'set rgb 45 229 188 0'
'set rgb 46 229 221 0'
'set rgb 47 210 229 0'
'set rgb 48 195 229 0'
'set rgb 49 145 229 0'
'set rgb 50 0 88 208'
'set rgb 51 0 116 216'
'set rgb 52 0 144 224'
'set rgb 53 0 172 232'
'set rgb 54 0 200 240'
'set rgb 55 0 228 248'
'set rgb 56 0 255 255'
'set rgb 57 0 255 176'
'set rgb 58 128 255 64'
'set rgb 59 192 255 0'

'sdfopen http://' base '/gfs_0p50/gfs' date '/gfs_0p50_' hour 'z'
if ( rc ); return; endif

'set t 1'
'set lat -40 -10'
'set lon 280 320'
'set grads off'
'set parea 1.5 9.5 .1 8.1'

'define precip= sum(const(acpcpsfc,0,-u),t=' offs - 5 ',t=' offs + 1 ',2)'

'set gxout shaded'
'set clevs 0 10 15 20 25 30 35 40 45 50 55 60 70 80 90 100 110 120 130'
'set ccols 0 59 58 57 56 55 54 53 52 51 50 49 48 47 46 45 44 43 42 41 40'
'd precip'

'set line 1 1 10'
'draw shp /home/maxi/workspace/gfs/cdp/cdp.shp'

'set line 1 5 9'
'draw shp /home/maxi/workspace/gfs/provincias/provincias.shp' 

'set string 1 bc 6'
'set strsiz .15 .18'
'draw string 5.5 8.2 GFS ' year '-' mon '-' day ' ' hour 'Z, PRECIPITACION DIARIA, +' valid 'h'

'set parea 9.7 9.9 .3 7.9'
'set frame on'
'set gxout contour'
'set t 1 2'
'set lon 0'
'set lat 0 84.999999'
'set xyrev on'
'set gxout shaded'
'set clevs 0 .1 .2 .5 1 2 3 4 5 7 10 15 20 25 30 40 50 60 70 80'
'set ccols 0 59 58 57 56 55 54 53 52 51 50 49 48 47 46 45 44 43 42 41 40'
'set ylpos 0 r'
'set ylint 5'
'set ylab %2.0f'
'set xlab off'
'set grid horizontal 1 16'
'd lat'

'set string 1 bl 5'
'set strsiz .1 .12'
'draw string 10 8.1 mm'

'printim precip.' year '-' mon '-' day '.' hour 'z+' valid '.png x1100 y850'

'quit'
