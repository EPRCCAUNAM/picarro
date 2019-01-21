import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
import datetime
import os
import sys



def toepoch(sdate,stime='00:00:00.000'):
        time1=datetime.datetime.strptime(sdate.strip()+stime.strip(), "%Y-%m-%d%H:%M:%S.%f")
        tnull=datetime.datetime(1970,1,1,0,0,0)
        return (time1-tnull).total_seconds()

#Especificar la ruta que se va a analizar/graficar:
#path='/home/michel/PICARRO/08/'

estacion = sys.argv[1]
huso_horario= sys.argv[2]


tnow=datetime.datetime.now()#+ datetime.timedelta(hours=9)
dia = tnow.date().day 
mes = tnow.date().month
anio = tnow.date().year

path='C:\UserData\DataLog_User\\%04i\\%02i\\%02i\\' % (anio,mes,dia)
print path


def read_picarrodata(filename_):
	print filename_
	f=open(filename_,'r')

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
                        print ' Exception could not append line'
	f.close()
	return picarrodata[1:]


file_list=os.listdir(path)
file_list=sorted(file_list)

for file_name in file_list:# [10:12]:
	print file_name
	try:
		picarrodata=np.append(picarrodata,read_picarrodata(path+file_name))
	except:
		picarrodata=read_picarrodata(path+file_name)
		print 'Exception', path+file_name

CO_Avg=round(np.average(picarrodata['CO']),3)
CO2_Avg=round(np.average(picarrodata['CO2']),1)
CH4_Avg=round(np.average(picarrodata['CH4']),3)


LST=[]
for i, Stime in enumerate(picarrodata['TIME']):
	Sdate=picarrodata['DATE'][i]
	#LST.append(datetime.datetime.strptime(Sdate.strip()+Stime,'%Y-%m-%d%H:%M:%S.%f')-datetime.timedelta(hours=6))
##	print Sdate.strip()+Stime.strip()
##	print "%Y-%m-%d%H:%M:%S.%f"
##	print "%s.%f"
	picarrodata['EPOCH_TIME'][i]=toepoch(Sdate,Stime)#datetime.datetime.strptime(Sdate.strip()+Stime.strip(), "%Y-%m-%d%H:%M:%S.%f").strftime("%S.%f")
	LST.append(datetime.datetime.fromtimestamp(picarrodata['EPOCH_TIME'][i]))


tmax = np.max(picarrodata['EPOCH_TIME'])
#itmax = np.argmax(picarrodata['EPOCH_TIME'])
itmin = np.argmin(picarrodata['EPOCH_TIME'])


Sdatetime=picarrodata['DATE'][itmin]
print "Max date in data set: ", Sdatetime
Sdate=picarrodata['DATE'][0]
tmin=toepoch(Sdate)#float(datetime.datetime.strptime(Sdatetime+'00:00', "%Y-%m-%d%H:%M" ).strftime("%dS.%f"))
print tmin
#timeinterval (60 = 1 minute, 300 = 5 min)
timeinterval = 300
print "Day begin:", tmin, datetime.datetime.fromtimestamp(tmin)
print "Finishing time:", tmax, datetime.datetime.fromtimestamp(tmax)
print "Time interval:", timeinterval/60,"min"

epoch = tmin


def promediar(arg_data):
	avg=arg_data[0]
	for rubro in arg_data.dtype.names:
		try :
			avg[rubro]=np.average(arg_data[rubro])
		except:
			a=0
	return avg

while epoch < tmax:
	indices=np.where(np.logical_and(epoch<picarrodata['EPOCH_TIME'],picarrodata['EPOCH_TIME']<epoch+timeinterval))[0]
	print datetime.datetime.fromtimestamp(epoch), len(indices) 
	try :
		print "Number of data averaged:",indices[1]
		avg = promediar(picarrodata[indices])
		avg['TIME'] = datetime.datetime.fromtimestamp(epoch).strftime('%H:%M:%S.%f')
		avg['DATE'] = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d')
		try:
                        avgdata=np.append(avgdata,avg)
                except:
                        avgdata=avg
	except:
		print "0"	
	epoch=epoch+timeinterval

avgdata=np.array(avgdata)

print 'CO avarage = ',CO_Avg,' ppm'
print picarrodata.dtype.names[18],' avarage = ',CO2_Avg,' ppm'
print 'CH4 avarage = ',CH4_Avg,' ppm'


LST_avg=[]
#for u in range(0,len(avgdata)):
for u, Avgtime in enumerate(avgdata['TIME']):
        Avgdate=avgdata[u]['DATE']
        #Avgtime=avgdata[u]['TIME']
        print Avgdate.strip()+Avgtime, Avgdate, Avgtime
        
        #avgdata[u]['EPOCH_TIME'][u]=datetime.datetime.strptime(Avgdate.strip()+Avgtime, '%Y-%m-%d%H:%M:%S.%f').strftime('%S.%f')
        LST_avg.append(datetime.datetime.fromtimestamp(avgdata[u]['EPOCH_TIME'])+datetime.timedelta(hours=0
                                                                                                    ))



# write
###############

def write_file(arg_data,arg_file):
        print 'i am writing', arg_file
	f=open(arg_file,'w')
	f.write("RUOA estacion: "+estacion.upper()+". Horario: "+huso_horario+" (www.ruoa.unam.mx) \r\n")
	for rubro in arg_data.dtype.names:
		f.write("%s\t" % (rubro))
	f.write("\r\n")
	for i in range(len(arg_data[arg_data.dtype.names[0]])):
		for rubro in arg_data.dtype.names:
			f.write("%s\t" % (arg_data[i][rubro]))
		f.write("\n")
	f.close()


write_file(avgdata,'avg\\'+str(Sdatetime) + '_'+estacion+'_avg.txt')


