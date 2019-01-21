#Este programa lee los datos entrantes de las estaciones con analizadores PICARRO y grafica un dia de datos. 
#Necesita un argumento para la estacion e.g. >picarro_plot_actual.py unam
#Se corre cada minuto al ser llamado por estaciones.py a traves de >crontab -e

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
import datetime
import os
import sys


estacion = sys.argv[1]
#Especificar la ruta que se va a analizar/graficar:

#path='/var/www/Datos/'+estacion+'/gei/'
path='/home/gei/data/'+estacion+'/'

tnow = datetime.datetime.now() 
dia = tnow.date().day
mes = tnow.date().month
anio = tnow.date().year

tayer= tnow-datetime.timedelta(hours=24) 
diaayer = tayer.date().day
mesayer = tayer.date().month
anioayer = tayer.date().year

#print(path)
filehoy = '%04i-%02i-%02i_%s_avg.txt' % (anio,mes,dia,estacion)
#print(filehoy)
fileayer = '%04i-%02i-%02i_%s_avg.txt' % (anioayer,mesayer,diaayer,estacion)
#print(fileayer)

Sdatetime = '%04i-%02i-%02i' % (anio,mes,dia)


def read_avgdata(filename_):
	#print(filename_)
	f=open(filename_,'r')
	print(f.readline())
	header=f.readline().split()
 
	position=f.tell()
	f.seek(0,2)
	end_position=f.tell()
	f.seek(position,0)

	var_type=[]
	for i in range(len(header)):
		if i==0: 
			var_type.append((header[i],str,10))
		elif i==1:
			var_type.append((header[i],str,12))
		else:
			var_type.append((header[i],float,1))
	
	picarrotype=np.dtype(var_type)
	picarrodata=np.zeros(1,dtype=picarrotype)
	singledata_line=picarrodata[0]

	while f.tell() < end_position:
		line=f.readline().split()
	
		try:
                        for i, single_header in enumerate(header):
                                singledata_line[single_header]=line[i]	
                        picarrodata=np.append(picarrodata,singledata_line)
		except:
			print(' Exception could not append line')
	f.close()
	return picarrodata[1:]

avgdata = read_avgdata(path+fileayer)
#print(len(avgdata))
avgdata=np.append(avgdata,read_avgdata(path+filehoy))
#print(len(avgdata))

CO_Avg=round(np.average(avgdata['CO']),3)
CO2_Avg=round(np.average(avgdata['CO2']),1)
CH4_Avg=round(np.average(avgdata['CH4']),3)


LST_avg=[]

for u, Avgtime in enumerate(avgdata['TIME']):
	Avgdate=avgdata[u]['DATE']
	#print(Avgdate.strip()+Avgtime, Avgdate, Avgtime)
	LST_avg.append(datetime.datetime.strptime(Avgdate.strip()+Avgtime,'%Y-%m-%d%H:%M:%S.%f'))
tmax = LST_avg[-1]
tmin = tmax-datetime.timedelta(hours=24)

#print('tmin = %s \n tmax=%s \n tnow= %s \n tayer= %s' %(tmin, tmax, tnow, tayer))


# PLOTS
###############
bbox_props = dict(boxstyle="round,pad=0.4",fc="w",lw=0)

# CO2
fig=plt.figure()
plt.plot(LST_avg,avgdata['CO2'])
hfmt = dates.DateFormatter('%H:%M')
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(hfmt)
plt.xlim(tmin,tmax)
plt.ylim(350,500)
plt.grid()
fig.suptitle('CO2 en '+estacion.upper()+', ' + str(Sdatetime))
plt.xlabel('Fecha Hora [UT-06]')
plt.ylabel('Concentracion [ppm]')
plt.xticks(rotation='vertical')
plt.subplots_adjust(bottom=.3)

ax.text(0.3,0.1,'Promedio ultimas 24h: ' + str(CO2_Avg) + ' ppm',ha='left',va='center',size=12,transform=ax.transAxes,bbox=bbox_props)
ax.text(0.3,0.18,'Hora actual: ' + str(tnow.strftime('%H:%M')),ha='left',va='center',size=12,transform=ax.transAxes,bbox=bbox_props)

plt.savefig(path+'/plots/'+str(Sdatetime) + '_CO2_'+estacion+'.png')
plt.savefig(path+'/plots/'+'CO2_'+estacion+'.png')
#plt.show()

# CH4
fig=plt.figure()
plt.plot(LST_avg,avgdata['CH4'])
hfmt = dates.DateFormatter('%H:%M')
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(hfmt)
plt.xlim(tmin,tmax)
plt.ylim(0.5,3)
plt.grid()
fig.suptitle('CH4 en '+estacion.upper()+', ' + str(Sdatetime))
plt.xlabel('Fecha Hora [UT-06]')
plt.ylabel('Concentracion [ppm]')
plt.xticks(rotation='vertical')
plt.subplots_adjust(bottom=.3)

ax.text(0.3,0.1,'Promedio ultimas 24h: ' + str(CH4_Avg) + ' ppm',ha='left',va='center',size=12,transform=ax.transAxes,bbox=bbox_props)
ax.text(0.3,0.18,'Hora actual: ' + str(tnow.strftime('%H:%M')),ha='left',va='center',size=12,transform=ax.transAxes,bbox=bbox_props)

plt.savefig(path+'/plots/'+str(Sdatetime) + '_CH4_'+estacion+'.png')
plt.savefig(path+'/plots/'+'CH4_'+estacion+'.png')
#plt.show()

