# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 23:11:57 2017

@author: Maria
"""

import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import glob


#reading multiple files into a sigle frame
#

#path =r'C:\Users\Maria\Dropbox_gm\Dropbox\2017\SPACE WEATHER\ictp paper\magnetic field\estaciones seleccionadas'
path =r'/home/gachi/Dropbox/2017/SPACE WEATHER/ictp paper/magnetic field/estaciones seleccionadas'
allFiles = glob.glob(path + "/pil*.min")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=24,sep='\s+')
    list_.append(df)
    
frame = pd.concat(list_)

#print (list_)
frame.columns=['FECHA','HOUR','DOY','X','Y','Z','G','?']
#print(frame.dtypes)

#New frame with columns DATE, TIME,DOY

nframe=frame.iloc[:,0:5]
#print(nframe)

#mising data treatment
#setting 99999.00 to NaN to avoid in calculation
#loc ensures to work with an unike nframe frame 

nframe.loc[nframe['X'] == 99999.00,'X'] = np.nan
nframe.loc[nframe['Y'] == 99999.00,'Y'] = np.nan



#print(nframe.head(100))

#adding new calcullated column called H

nframe['H']=(nframe.X**2+nframe.Y**2)**0.5

#print(nframe.head(100))

#Grouping
#Obtaining AVG for each time
byHOUR = nframe.groupby(['HOUR'])['H'].mean()


#head:Returns first n rows
#print(byHOUR.head(10000))

# group into frame
QDC = byHOUR.to_frame()
#print(QDC.head(10))
#Plotting Data


fig=QDC['H'].plot(title='Horizontal component of magnetic field',color='k',style='--')
n = 3

ticks = fig.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in fig.xaxis.get_ticklabels()]
fig.xaxis.set_ticks(ticks[::n])
fig.xaxis.set_ticklabels(ticklabels[::n])
fig.set_xlabel("Hour")
fig.set_ylabel("H [nT]")


#fig.plot(style='k-', color='k');


#Obtaining disturbed data to compare
file_=r'/home/gachi/Dropbox/2017/SPACE WEATHER/ictp paper/magnetic field/estaciones seleccionadas/0210/pil20131002dmin.min'
frame = pd.DataFrame()
#changed header 25 --> 24
frame= pd.read_csv(file_,index_col=None, header=24,sep='\s+')


#print (list_)
frame.columns=['FECHA','HOUR','DOY','X','Y','Z','G','?']
#print(frame.dtypes)

#New frame with columns DATE, TIME,DOY

nframe=frame.iloc[:,0:5]
#print(nframe)

#mising data treatment
#setting 99999.00 to NaN to avoid in calculation
#loc ensures to work with an unike nframe frame 

nframe.loc[nframe['X'] == 99999.00,'X'] = np.nan
nframe.loc[nframe['Y'] == 99999.00,'Y'] = np.nan

#print(nframe.head(100))

#adding new calcullated column called H

nframe['H']=(nframe.X**2+nframe.Y**2)**0.5
nframe['H'].plot(color='k')

#Plotting Data





