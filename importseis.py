#!/usr/bin/env python

# Script to import and plot seismic data. A prompt is used to
# ask the user the time range to plot, and from which station.
# Each file contains a single column, containing an hour of seismic
# data, with a sample interval of 100Hz.
# Plotting data as rows of hour-long subplots

# Importing modules
import numpy as np
import os
import datetime as dt
import time
import obspy
import matplotlib.pyplot as plt

#%% Asking user for range of files to open
first_date = str(raw_input("First date to copy (dd/mm/yyyy): "))
last_date = str(raw_input("Last date to copy (dd/mm/yyyy): "))

first_hour = str(raw_input("First hour to copy (hh): "))
last_hour = str(raw_input("Last hour to copy (hh): "))

station = str(raw_input("Station (RETU, ARA2 or POND)? "))

if station == 'ARA2':
	component = "SHZ"
elif station == 'RETU':
	component = "SHZ"
elif station == 'POND':
	component = str(raw_input("Component (HHZ, HHE, HHN)? "))

#%%
# Combining strings for use when calculating UT time
first_date_hour = first_date + " " + first_hour
last_date_hour = last_date + " " + last_hour

#Calculating UT time of first and last hour-long file to open (start time of file)
first_hour_ut = time.mktime(dt.datetime.strptime(first_date_hour, "%d/%m/%Y %H").timetuple())
last_hour_ut = time.mktime(dt.datetime.strptime(last_date_hour, "%d/%m/%Y %H").timetuple())

#Creating an array of UT times, where each time refers to a single file
hour_list_ut = np.arange(first_hour_ut, last_hour_ut + 3600, 3600);
# Number of files to open
num_hours = len(hour_list_ut)

# Parameters required for seismic data
sample_int = 100 # sample interal (Hz)
timesecs= np.linspace(0,3599.99,360000) # time of each sample in seconds
timemins=timesecs/60 # time of each sample in minutes

st = obspy.read()

for k in range(0,num_hours): # Looping through to open each hour-long file incrementally, and append the data to an array.
	dd = int(dt.datetime.fromtimestamp(int(hour_list_ut[k])).strftime('%d')) # Temporal information of each file, extracted from UT time
	mm = int(dt.datetime.fromtimestamp(int(hour_list_ut[k])).strftime('%m'))
	yyyy = int(dt.datetime.fromtimestamp(int(hour_list_ut[k])).strftime('%Y'))
	hh = int(dt.datetime.fromtimestamp(int(hour_list_ut[k])).strftime('%H'))
	# File name has temporal information
    filepath = '/nfs/a136/SeismicData/Tungurahua/1_hour_ascii/' + station + '/' + component + '/' + "%04d" % yyyy + '/' + "%02d" % mm + '/' + "%02d" % dd + '/' + 'EC.' + station + '.' + component + '.D.' + "%04d" % yyyy + '.' + "%02d" % mm + '.' + "%02d" % dd + '.' + "%02d" % hh + '.ascii'
	with open(filepath) as f: # opening file
		linesafterfirst = np.array(f.readlines()[1:]).astype(np.float) # creating array of data in each file
	tror = linesafterfirst - np.nanmean(linesafterfirst) # Removing offset from data (mean)
	tr = obspy.Trace(tror) # Creating trace
    # Updating trace headers
	tr.stats.sampling_rate = sample_int
	tr.stats.station = station + "_" + component
	tr.stats.starttime = hour_list_ut[k]
    # Appending trace to one long string to be plotted.
	st.append(tr)	

# Removing suprplus data loaded automatically by ObsPy
for tr in st.select(component="E"):
    st.remove(tr)  
for tr in st.select(component="N"):
    st.remove(tr)  
for tr in st.select(component="Z"):
    st.remove(tr)  

#%% Plotting data

# Plot dimensions
width = 0.8
bottom = 0.1
height = 0.8/num_hours # Height of each subplot, function of number of hours
left = 0.12
top = bottom + (num_hours * height)

fig = plt.figure()

for k in range(0,num_hours): # Plotting each hour as a separate subplot
	ax = plt.subplot(num_hours,1,k+1)
	bottomk = top - (height*(k+1))
	pos = [left, bottomk, width, height] 
	ax.set_position(pos)
	if k != (num_hours-1):
		ax.set_xticklabels([])
	ax.set_yticklabels([])
	plt.plot(timemins,st[k],color='black')
	plt.ylabel(dt.datetime.fromtimestamp(int(hour_list_ut[k])).strftime('%H:%M'),rotation=0, labelpad=20, fontsize=8)
	plt.ylim([-2100, 2100])

plt.xlabel('Time in hour (minutes)', fontsize=8)
plt.tick_params(axis='both', which='major', labelsize=8)
filepath = os.path.abspath
filename = "/nfs/student42/eelhm/My_Documents/Data/Images/" + station + "." + dt.datetime.fromtimestamp(int(first_hour_ut)).strftime('%Y.%m.%d.%H') + ".to." + dt.datetime.fromtimestamp(int(last_hour_ut)).strftime('%Y.%m.%d.%H') + ".png"
fig.text(0.02, 0.5, 'Hour (UTC)', va='center', rotation='vertical', fontsize=8)
#plt.savefig(filename)

plt.show()





