import scipy
import numpy
import wavelet_entropy as waen
import EEGFileList as flist
from scipy import signal 
import pandas as pd
from pandas import read_csv

"""
Read txt datafiles: 
    cut the data into 5s/peice. The data is totally aroundd 14min long. 
    Consisit of 1min relax, 4min open eyes, 1min relax, 4min close eyes, 1min relax, 4min open eyes.
    use the signal between 2min-4min and 6.5min-8.5min
"""

# filter the data at 50Hz
def Notch_filter(sig_data,sample_rate):
    fr=50
    fs=sample_rate
    Q=10
    b,a = signal.iirnotch(fr,Q,fs)
    filted_data=scipy.signal.filtfilt(b,a,sig_data)
    b, a = signal.butter(8, [0.004,0.86], 'bandpass')   
    filtedData = signal.filtfilt(b, a, filted_data)  
    return filtedData


# FFT with a hamming window
def FFT_ham(sig_data,sample_rate):
    N=5*sample_rate
    hamming_win=signal.hamming(N)
    sig_win=sig_data*hamming_win
    sig_fft=numpy.fft.fft(sig_win)
    f=numpy.fft.fftfreq(N, 1/sample_rate)
    return sig_fft, f


def standardize(x):
    # y=x-x.mean()
    arange=x.max()-x.min()
    y=(x-x.mean())/arange
    return y

def normalize(x):
    arange=x.max()-x.min()
    y=(x-x.min())/arange
    return y

def normalizelist(x):
    # y=x-x.mean()
    arange=max(x)-min(x)
    y=(x-min(x))/arange
    return y

# get 24 features for data in a file list
def GetFeature(file_list,x1,x2,kval,delta,theta, alpha, beta, gamma, fi, KSS,WE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=None,device=None,device_name=None):
    for file in file_list:
        print(file)
        if(file_list==flist.FATIGUE_EM or file_list==flist.WAKE_EM):
            src = read_csv(file)
            EEG = (src["EEG.F3"] +src["EEG.F4"])/2.0
            # print("111",EEG.shape)
            # Resample the EEG signal of EMOTIV to 256Hz
            EEG = signal.resample(EEG, len(EEG)*2)
            # print("111",EEG.shape)
            # Refresh the Sample rate 
            sample_rate=256

        elif(file_list==flist.FATIGUE_UL or file_list==flist.WAKE_UL):
            src = read_csv(file)
            # Reshape the EEG signal array of UmindLite 
            EEG = [src['C1'],src['C2'],src['C3'],src['C4']]
            EEG=numpy.reshape(numpy.array(EEG),4*len(EEG[0]))
        else:
            EEG = numpy.loadtxt(file)
        
        filtered_data=numpy.zeros(sample_rate*5)

        # Cut Raw Signal to 5s pieces
        for i in range(x1,x2):
            eegdata=EEG[i*sample_rate*5:(i+1)*sample_rate*5]
            # print(eegdata.shape)
            eegdata=standardize(eegdata)
            #eegdata=normalize(eegdata)
            # print(eegdata.mean())
            filtered_data=Notch_filter(eegdata,sample_rate)
            # Filter signal to only have the information of 0-128Hz 
            if(sample_rate==512):
                b, a = signal.butter(8, 0.5, 'lowpass')  
                filtered_data = signal.filtfilt(b, a, filtered_data) 
            # else:
            #   b, a = signal.butter(8, 0.5, 'lowpass')   
            #   filtered_data = signal.filtfilt(b, a, filtered_data)  
            #   b, a = signal.butter(8, [0.004,0.5], 'bandpass')   
            #   filtered_data = signal.filtfilt(b, a, filtered_data)  

            # Get Entropy and RWE
            we,re2,re3,tse,gentse,Pi=waen.WE(filtered_data)
            RWE.append(Pi)
            WE.append(we)
            RE2.append(re2)
            RE3.append(re3)
            TsE.append(tse)
            GenTsE.append(gentse)
            if(device_name!=None):
                device.append(device_name)

            # Get FFT in range 0-128Hz
            sig_fft,freq_fft=FFT_ham(filtered_data,sample_rate)
            eeg_power=numpy.abs(sig_fft)**2
            eeg=eeg_power[:int(sample_rate*5/2)]
            delta.append(numpy.mean(eeg[int(0.5/128*(sample_rate*5/2)):int(4/128*(sample_rate*5/2))]))
            theta.append(numpy.mean(eeg[int(4/128*(sample_rate*5/2)):int(8/128*(sample_rate*5/2))]))
            alpha.append(numpy.mean(eeg[int(7.5/128*(sample_rate*5/2)):int(13/128*(sample_rate*5/2))]))
            beta.append(numpy.mean(eeg[int(13/128*(sample_rate*5/2)):int(30/128*(sample_rate*5/2))]))
            gamma.append(numpy.mean(eeg[int(30/128*(sample_rate*5/2)):int(44/128*(sample_rate*5/2))]))
            fi.append(numpy.mean(eeg[int(0.85/128*(sample_rate*5/2)):int(110/128*(sample_rate*5/2))]))

            # KSS.append(KSS_val)
            KSS.append(kval)

    return delta,theta,alpha,beta,gamma,fi,KSS, WE,RE2,RE3,TsE,GenTsE,RWE,device
