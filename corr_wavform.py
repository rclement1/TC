
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

# In[3]:

#get_ipython().magic(u'matplotlib nbagg') ## comment this out to run for just python
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from obspy.core import read, UTCDateTime
from obspy import Trace, Stream


# In[5]:

# load in the data and change the start and end times (limits the data)
st = read("HSR.UW..EHZ.2004.350.000000.SAC") # TC
#st = read("S:/HSR.UW..EHZ.2004.350.000000.SAC") # local
full_time_start = UTCDateTime("2004-12-15T23:16:10")
full_time_end = UTCDateTime("2004-12-15T23:30:30")
st_full = st.slice(full_time_start,full_time_end)


# In[6]:

# normalize the data and select window length
st_full_n = st_full[0].normalize(norm=None)
window_length = 10000
correlation_value = 1


# In[7]:

# function which convolves the window with the selected window length
# inputs:  sig = selected signal
#          win_len = window length 
# outputs: xcorr_dat = cross correlation data
#          index = array holding the iteration number and position where
#                  the cross correlation value is above a certain value
def cor(sig, win_len, cor_val):

    #sig = np.zeros([50])
    fft_sigb_1 = np.zeros([len(sig)])
    xcorr_dat = np.zeros([len(sig),len(sig)])
    xcorr_dat_n = np.zeros([len(sig),len(sig)])
    xcorrs = []
    # NB num is to what maximum will the window operate to
    # i.e., if len(sig) = 201 and win_len = 50, then the window
    # would iterate through until the 150th point
    num = (len(sig)-win_len)+1
    #num = 1
    
    for i in range(0,num,1):
        #sigb= sig[i:i+3]
	print i
        sigb = sig[i:i+win_len]
        #xc = signal.fftconvolve(sig,sigb,'same')
        xc = signal.correlate(sig, sigb, mode='same')
        xcorrs.append(xc)
        
        # sorts the cross-correlations into the array xcorr_dat[x,y]
        # where x is the iteration and j is the signal
        for j in xcorrs:
            xcorr_dat[i] = j
            
    # find where the cross-correlation value is above a certain value
    # index[0] is the iteration array
    # index[1] is the position at which the xcorr is above that value
    # eg index[0] = 8, index[1] = 11 -> iteration 8 has a xcorr value
    # of >0.5 at point 11
    index = np.where(xcorr_dat > cor_val)
    return [xcorr_dat, index]


# In[8]:

# this is where the magic happens..
[xcorr_dat, index] = cor(st_full_n, window_length, correlation_value)

print("iteration number:")
print(index[0])
print("position of xcorr > value:")
print(index[1])
print("xcorr value:")
print(xcorr_dat[index[0],index[1]])

# finds where the index of the maximum xcorr value window is
# then creates array with just that window in it
max_xcorr = np.where(xcorr_dat == max(xcorr_dat[index[0],index[1]]))[0][0]
best_win = np.repeat(float('NaN'),len(st_full_n))
best_win[max_xcorr:max_xcorr+window_length] = st_full_n[max_xcorr:max_xcorr+window_length]


# In[19]:

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
plt.savefig("/exports/home/s1016630/" + file_name + "_1.png")
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
plt.savefig("/exports/home/s1016630/" + file_name + "_2.png")

#plt.savefig("/exports/home/s1016630/" + file_name + ".png")


# In[ ]:



