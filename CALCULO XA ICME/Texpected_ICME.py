#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 11:22:03 2017

@author: gachi
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 11:50:51 2017

@author: gachi
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:17:44 2017

@author: Maria Graciela Molina
"""

""" 
ARCHIVO In_D_V_T 
Corresponds to the file without header
Each bad measurment use to be  -1.00000E+31 in the original, 
while in the parsed version it has 0.00 instead (to ease the processing)
Each row is separated by ','
 
ROWS:

1. Time, beginning of interval
2. Solar Wind Proton Number Density, scalar
NOTES:  Np is the proton number density in units of cm-3, as calculated by integrating the ion distribution function.
3. Solar Wind Bulk Speed
NOTES:  Vp is the solar wind proton speed, or more generally just the solar wind (bulk) speed. It is obtained by integrating the ion (proton) distribution function.
4. radial component of the proton temperature
NOTES:  The radial component of the proton temperature is the (1,1) component of the temperature tensor, along the radial direction. It is obtained by integration of the ion (proton) distribution function.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as pp
#mtick to give format to yticks in the plots
import matplotlib.ticker as mtick

from datetime import datetime

##Using array for the measurments so it is easear to do math
#D=np.array([],float)
#V=np.array([],float)
#T=np.array([],float)
##Using list for datetime (dt)
##dt=[]
#dt=np.array([],dtype='datetime64')

#Num_lines=0


def MakeFrame():
    #Creating a data frame from a csv text file
    # When read data, automatically nan values are set where value is -1.00000E+31

    file_=r'AC_H0_SWE_1619899_parsed.txt'
    foriginal = pd.DataFrame()
    foriginal= pd.read_csv(file_,index_col=None,sep='\s+',na_values=['-1.00000E+31'])
    #here columns are created
    foriginal.columns=['Date','Time','D','V','T']
    #print(frame)
    fnew=pd.DataFrame()
    fnew['DateTime']=pd.to_datetime(foriginal['Date'] + ' ' + foriginal['Time'])
    fnew['D']=foriginal['D']
    fnew['V']=foriginal['V']
    fnew['T']=foriginal['T']
    fnew.index = fnew['DateTime']
#    print (fnew)
    
    return fnew

#here frame from file is created
df=MakeFrame()


##in this step, data is groupped by year, month,day,hour
grupo=df.groupby([df.index.year, df.index.month, df.index.day,df.index.hour])
#compute hourly mean value for each day
df_mean=grupo.mean()    
#print df.DateTime



#compute numerical derivate using discrete difference method
temperatura=np.array(df_mean['T'])
velocidad=np.array(df_mean['V'])
densidad=np.array(df_mean['D'])
#amount of computed days is len(temperatura)/23 --> in our case it gives 6
#do not use group.count because it does not count nan values ... carefull
#Nday will be used to plot
Ndays=len(temperatura)/24
#xticks=df_mean[df_mean.index.year]
#print xticks


#velocidad [km/s]
# methos diff uses for the first derivative out[n] = a[n+1] - a[n] so that:
#>>> x = np.array([1, 2, 4, 7, 0])
#>>> np.diff(x)
#array([ 1,  2,  3, -7])

derivada_V=np.diff(velocidad)


#In order to obten Texpected discrimination for compression and rarefactions
# derivada_V>=2.2E-4 --> compression
# derivada_V<=-2.2E-4 --> rarefaction
#If compression: Texp=640*V-1.56E5
#If rarefaction: Texp=459*V-1.18E5

#CALCULO DE TEXPECTED
Texp=np.array([],float)
Temp_selected=np.array([],float)
Dens_selected=np.array([],float)
Veloc_selected=np.array([],float)
index=0
for i in derivada_V:
    if i<=-2.2*10**(-4):
        Texp=np.append(Texp,459*velocidad[index+1]-1.18**5)
        Temp_selected=np.append(Temp_selected,temperatura[index+1])
        Dens_selected=np.append(Dens_selected,densidad[index+1])
        Veloc_selected=np.append(Veloc_selected,velocidad[index+1])
    if i>=2.2*10**(-4):
    #else:
        Texp=np.append(Texp,640*velocidad[index+1]-1.56**5)
        Temp_selected=np.append(Temp_selected,temperatura[index+1])
        Dens_selected=np.append(Dens_selected,densidad[index+1])
        Veloc_selected=np.append(Veloc_selected,velocidad[index+1])
    index=index+1



#PLOTS
#print len(Texp)
#print index
labels = ['05', '06', '07', '08','09','10']
x = np.linspace(0, Ndays-1, len(Texp))
pp.figure(figsize=(15,10))
#criterio Richardson Texp/2
pp.plot(x,Texp/2, label="Texp/2")
pp.plot(x,Temp_selected, label="Temp_selected")
pp.legend(bbox_to_anchor=(0.8, 1), loc=2, borderaxespad=0.,prop={'size': 14})
pp.xticks(np.arange(Ndays+1), labels)
pp.grid(True)
pp.xlabel('Day',fontweight='bold',fontsize=14)
pp.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e')) 
pp.gca().set_xlim([0,Ndays-1])
pp.ylabel('Temperature [K]',fontweight='bold',fontsize=14)
pp.title('Solar wind temperature analysis (October 2015)',fontweight='bold',fontsize=16)
pp.show()

x = np.linspace(0, Ndays-1, len(Texp))
pp.figure(figsize=(15,10))
pp.plot(x,Temp_selected/Texp)
pp.ylabel('Temp/Texp [K]',fontweight='bold',fontsize=14)
pp.grid(True)
pp.xlabel('Day',fontweight='bold',fontsize=14)
pp.title('Temperature/Texp',fontweight='bold',fontsize=14)
pp.show()


pp.figure(figsize=(15,10))
pp.subplot(3,1,1)
pp.title('Temperature',fontweight='bold',fontsize=14)
pp.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e')) 
pp.gca().set_xlim([0,Ndays-1])
pp.plot(x,Temp_selected-Texp/2)
pp.ylabel('Temp -Texp/2 [K]',fontweight='bold',fontsize=14)
pp.subplot(3,1,2)
pp.plot(x, Veloc_selected)
pp.title('Solar Wind Bulk Speed',fontweight='bold',fontsize=14)
pp.ylabel('[Km/s]',fontweight='bold',fontsize=10)
pp.gca().set_xlim([0,Ndays-1])
pp.subplot(3,1,3)
pp.plot(x, Dens_selected)
pp.title('Solar Wind Proton Number Density',fontweight='bold',fontsize=14)

pp.gca().set_xlim([0,Ndays-1])


"""

pp.figure()
pp.scatter(Texp,Temp_selected)
pp.ylabel('Texp')
pp.grid(True)
pp.xlabel('T')
pp.show()

"""