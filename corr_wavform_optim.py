
# coding: utf-8

# Code will have a moving window which will be cross correlated with the entire dataset. At present, the output which is produced consists of 4 plots. 
# 
# 1 - Best cross correlation window (highest max value)
# 
# 2 - Window which had the best match
# 
# 3 - Full cross correlation (different iterations are different colours)
# 
# 4 - Full dataset with best window

# In[1]:

#get_ipython().magic(u'matplotlib nbagg') ## comment this out to run for just python
import matplotlib as mpl  # TC
mpl.use('Agg')   #TC
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from obspy.core import read, UTCDateTime
from obspy import Trace, Stream


# In[2]:

# load in the data and change the start and end times (limits the data)
st = read("HSR.UW..EHZ.2004.350.000000.SAC") # TC
#st = read("S:/HSR.UW..EHZ.2004.350.000000.SAC") # local
full_time_start = UTCDateTime("2004-12-15T23:16:10")
full_time_end = UTCDateTime("2004-12-15T23:20:20")
st_full = st.slice(full_time_start,full_time_end)


# In[12]:

# normalize the data and select window length
st_full_n = st_full[0].normalize(norm=None)
window_length = 100
correlation_value = 1


# In[81]:

def pairTraces(window_length, st_full_n):
    # prepares the trace array
    trace_list = [] #empty list
    corr_file = open('corrfile.txt','w') #opens the file for xcorr values
    corr_file.write("Cross-correlation values \n")
    trace_file = open('tracefile.txt','w') #opens the file for trace values
    trace_file.write("Trace values with a window of %s " % window_length                      + ", a start time of %s \n" % full_time_start +                      "and an end time of %s \n" % full_time_end)
    maxc_file = open('maxcorrs.txt','w') #opens the file for where the xcorr is > correlation value
    maxc_file.write("Values of cross-correlation which are higher than the threshold of : %s \n" % correlation_value                     + " and the index at which the value occurs \n")
    for i in range(len(st_full_n)-window_length):
        # loops through through whole dataset - window_length to prepare
        # the list
        trace_list.append(np.copy(st_full_n[i:i+window_length]))
        
    for ii in range(len(trace_list)):
        # loops through each trace and does the cross-correlation via 
        # the cor function and stores the trace
        xc = cor(trace_list[ii],st_full_n,corr_file,maxc_file)
        trace_file.write("%s \n" % str(trace_list[ii])) # writes the trace values to file   
    #corr_file.close()
    #trace_file.close()
    return trace_list, xc # returns the trace values to test that it works

def cor(trace1,st_full_n,corr_file,maxc_file):
    # performs the cross-correlation between the trace and the dataset and then
    # stores the correlation value and correlation values above the threshold
    xc = signal.correlate(trace1, st_full_n, mode='same')
    storeCorrs(xc, corr_file) #calls the storeCorrs function
    findValues(xc,correlation_value,maxc_file) #calls the findValues function
    return xc
    
def storeCorrs(xc, corr_file):
    # stores the cross-correlation values in a text file
    return corr_file.write("%s \n" % str(xc))

def findValues(xc, correlation_value,maxc_file):
    # stores the correlation values which are higher than the threshold in a text file
    index = np.where(xc > correlation_value)
    corr_vals = xc[index]
    return maxc_file.write("%s \t " % corr_vals + "%s \n" % index)

cor_trace_vals,xc = pairTraces(window_length,st_full_n)


# In[57]:

###################################################
###STILL TO IMPLEMENT BEST CORRELATION AND PLOTS### 
###################################################

# finds where the index of the maximum xcorr value window is
# then creates array with just that window in it
max_xcorr = np.where(xcorr_dat == max(xcorr_dat[index[0],index[1]]))[0][0]
best_win = np.repeat(float('NaN'),len(st_full_n))
best_win[max_xcorr:max_xcorr+window_length] = st_full_n[max_xcorr:max_xcorr+window_length]


# In[10]:

#plots and plots and plots
file_name = 'W' + str(window_length) + "_SD" + str(full_time_start.day) + "_ST" + str(full_time_start.time) + "_ED" + str(full_time_end.day) + "_ET" + str(full_time_end.time)
plt.figure(1)
plt.subplot(211)
plt.title("Best cross correlation window (highest max value)")
# best cross-correlation window
plt.plot(xcorr_dat[max_xcorr])
plt.subplot(212)
plt.title("Best match window")
# window which had the best match
ax1 = plt.plot(st_full_n[max_xcorr:max_xcorr+window_length])
#plt.savefig("/exports/home/s1016630/" + file_name + "_1.png")
plt.figure(2)
plt.subplot(211)# full cross correlation
plt.title("Full cross-correlation")
plt.plot(xcorr_dat)
ax2 = plt.subplot(212)
plt.title("Full dataset with best window in red")
# plots the full dataset with the best window overlayed in red
plt.plot(st_full_n)
plt.plot(best_win,'r')
#ax2.autoscale(enable=False)
#plt.savefig("/exports/home/s1016630/" + file_name + "_2.png")
plt.show()
#plt.savefig("/exports/home/s1016630/" + file_name + ".png")


# In[ ]:



