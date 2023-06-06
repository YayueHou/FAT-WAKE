# not enough variance to choose
# wavelet entropy python
import numpy as np
import pywt

def WE(sig, wavelet = 'db4'):
    n = len(sig)
    
    #sig = y
    
    ap = {}
    coeffs= pywt.wavedec(sig, wavelet,level=5)
    # coeffs= pywt.wavedec(sig, wavelet,mode='smooth',level=6)
    a6,d5,d4,d3,d2,d1=coeffs
  
    #This is to remove artifects
    d1=pywt.threshold(d1, np.mean(d1), mode='soft', substitute=0)
    d2=pywt.threshold(d2, np.mean(d2), mode='soft', substitute=0)
    d3=pywt.threshold(d3, np.mean(d3), mode='soft', substitute=0)
    d4=pywt.threshold(d4, np.mean(d4), mode='soft', substitute=0)
    d5=pywt.threshold(d5, np.mean(d5), mode='soft', substitute=0)

  #  This is the reconstruction process 
  #  print("-----------------------")
  #  print(d1)
  #  print(d2)
  #  print(d3)
  #  print(d4)
  #  print(d5)
  #  print(a6)
  #  A5=pywt.upcoef('a',a5,'db5',take=n)
  #  D5=pywt.upcoef('d',d5,'db5',take=n)
  #  D1=pywt.upcoef('d',d1,'db5',take=n)
  #  D2=pywt.upcoef('d',d2,'db5',take=n)
  #  D3=pywt.upcoef('d',d3,'db5',take=n)
  #  D4=pywt.upcoef('d',d4,'db5',take=n)
  #  print(D1)
  #  print(D2)
  #  print(D3)
  #  print(D4)
  #  print(D5)
  #  print(A5)

  #  S5=A5+D5
  #  S4=A5+D5+D4
  #  S3=A5+D5+D4+D3
  #  S2=A5+D5+D4+D3+D2
  #  S1=A5+D5+D4+D3+D2+D1


    E1 = np.sqrt(np.sum(np.power(d1,2))/len(d1)) #0-64
    E2 = np.sqrt(np.sum(np.power(d2,2))/len(d2)) #0-32
    E3 = np.sqrt(np.sum(np.power(d3,2))/len(d3)) #0-16
    E4 = np.sqrt(np.sum(np.power(d4,2))/len(d4)) #0-8
    E5 = np.sqrt(np.sum(np.power(d5,2))/len(d5)) #0-4


    Eto=E1+E2+E3+E4+E5
    Pi = np.zeros(5)

    Pi[0]=E1/Eto
    Pi[1]=E2/Eto
    Pi[2]=E3/Eto


    Pi[3]=E4/Eto
    Pi[4]=E5/Eto

    # Wavelet entropy     
    WE = - np.sum(np.dot(Pi,np.log(Pi)))
    
    # Renyi entropy
    #2 level
    RE2 = 1/(1-2)*np.log(np.sum(np.power(Pi,2)))

    #3 level
    RE3 = 1/(1-3)*np.log(np.sum(np.power(Pi,3)))

    # Tsallis wavwlet entropy
    TsE= 1/(2-1)*np.sum(Pi-np.power(Pi,2))

    # Generalized Tsallis wavwlet entropy
    GenTsE=1/(2-1)*(1-(np.sum(np.power((np.power(Pi,0.5)),-2))))
    
    return WE,RE2,RE3,TsE,GenTsE,Pi

