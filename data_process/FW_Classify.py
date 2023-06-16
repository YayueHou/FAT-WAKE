import numpy
import preprocess as pre
import FW_Class_SVM_KNN as fwcl
import EEGFileList as eeg
import eegcnn as ecn
import mlpeeg as mlp

# Use the following variables to select class options
FW_BRAINLINK_CLASS=0
FW_EMOTIV_CLASS=0
FW_UMINDSLEEP_CLASS=0
FW_UMINDLITE_CLASS=0
FW_ALL_CLASS=0
FW_CLOSE_EYE=0
FW_OPEN_EYE=0
FW_ALL_EYE=0

FW_TGAM_EAR=0
FW_TGAM_FRONT=1
FW_TGAM_ALL=0

KSS=[]

delta, theta, alpha, beta, gamma, fi, KSS = [], [], [], [], [], [], []
SE,RE2,RE3,TsE,GenTsE= [],[],[],[],[]
A5,D5,D4,D3,D2,D1,RWE=[],[],[],[],[],[],[]
Device=[]

# BrainLink
# BrainLink open eyes
if((FW_BRAINLINK_CLASS or FW_ALL_CLASS) and (FW_OPEN_EYE or FW_ALL_EYE)):
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_BL,24,48,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=512,device=Device,device_name='Open_Eyes')
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_BL,24,48,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=512,device=Device,device_name='Open_Eyes')

# BrainLink close eyes
if((FW_BRAINLINK_CLASS or FW_ALL_CLASS) and (FW_CLOSE_EYE or FW_ALL_EYE)):
    delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_BL,78,102,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=512,device=Device,device_name='Close_Eyes')
    delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_BL,78,102,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=512,device=Device,device_name='Close_Eyes')


# UmindSleep
# UmindSleep open eyes
if((FW_UMINDSLEEP_CLASS or FW_ALL_CLASS) and (FW_OPEN_EYE or FW_ALL_EYE)):
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_US,24,48,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Open_Eyes')
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_US,24,48,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Open_Eyes')

# UmindSleep close eyes
if((FW_UMINDSLEEP_CLASS or FW_ALL_CLASS) and (FW_CLOSE_EYE or FW_ALL_EYE)):
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_US,78,102,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Close_Eyes')
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_US,78,102,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Close_Eyes')


# EMOTV
# EMOTV open eyes
if((FW_EMOTIV_CLASS or FW_ALL_CLASS) and (FW_OPEN_EYE or FW_ALL_EYE)):
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_EM,24,48,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=128,device=Device,device_name='Open_Eyes')
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_EM,24,48,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=128,device=Device,device_name='Open_Eyes')

# EMOTIV close eyes
if((FW_EMOTIV_CLASS or FW_ALL_CLASS) and (FW_CLOSE_EYE or FW_ALL_EYE)):
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_EM,78,102,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=128,device=Device,device_name='Close_Eyes')
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_EM,78,102,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=128,device=Device,device_name='Close_Eyes')


# UmindLite
# UmindLite open eyes
if((FW_UMINDLITE_CLASS or FW_ALL_CLASS) and (FW_OPEN_EYE or FW_ALL_EYE)):
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_UL,24,48,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Open_Eyes')
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_UL,24,48,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Open_Eyes')

# UmindLite close eyes
if((FW_UMINDLITE_CLASS or FW_ALL_CLASS) and (FW_CLOSE_EYE or FW_ALL_EYE)):
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_UL,78,102,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Close_Eyes')
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_UL,78,102,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Close_Eyes')


# TGAM
# TGAM FONRT
if((FW_TGAM_FRONT or FW_TGAM_ALL)):
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_F_FAT,24,48,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Forehead FP1')
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_F_FAT,78,102,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Forehead FP1')

  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_F_WAK,24,48,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Forehead FP1')
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_F_WAK,78,102,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Forehead FP1')

# TGAM EAR
if((FW_TGAM_EAR or FW_TGAM_ALL)):
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_E_FAT,24,48,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L3')
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_E_FAT,78,102,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L3')

  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_E_WAK,24,48,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L3')
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_E_WAK,78,102,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L3')




delta = numpy.array(delta)  
theta = numpy.array(theta)    
alpha = numpy.array(alpha)    
beta = numpy.array(beta)    
gamma = numpy.array(gamma)    
fi = numpy.array(fi)    

RWE=numpy.transpose(numpy.array(RWE))

# Try to use RWE as power density (Accuracy increase but not mentioned in thesis)
# delta=RWE[7]+RWE[6]+RWE[5]
# theta=RWE[4]  # 4-8
# alpha=RWE[3]  # 8-16
# beta=RWE[2]   # 16-32
# gamma=RWE[0]+RWE[1] #64-128 32-64 



Sp =[delta, theta, alpha, theta/beta, theta/alpha, theta/fi, theta/alpha+beta+gamma, delta/alpha+beta+gamma, delta/alpha, delta/fi, delta/beta, delta/theta, theta/alpha+beta+theta, alpha/theta+alpha+beta, beta/theta+alpha+beta]
Entropy=[SE,RE2,TsE,GenTsE]
allf =[delta, theta, alpha, theta/beta, theta/alpha, theta/fi, theta/alpha+beta+gamma, delta/alpha+beta+gamma, delta/alpha, delta/fi, delta/beta, delta/theta, theta/alpha+beta+theta, alpha/theta+alpha+beta, beta/theta+alpha+beta,SE,RE2,TsE,GenTsE]
allf=numpy.array(allf)
y = numpy.transpose(numpy.array(KSS))
xi=numpy.transpose(numpy.vstack((allf,RWE)))

x=[]
x.append(numpy.transpose(numpy.array(Sp)))
x.append(numpy.transpose(RWE))
x.append(numpy.transpose(numpy.array(Entropy)))
x.append(numpy.hstack((numpy.transpose(allf),numpy.transpose(RWE))))

for t in range(len(x)):
  print(x[t].shape)
  svmacc=fwcl.FW_classby_SVM(x[t],y)
  knnacc=fwcl.FW_classby_KNN(x[t],y)
  print("SVM: acc: ",svmacc.mean(),"  std: ",svmacc.std())
  print("KNN: acc: ",knnacc.mean(),"  std: ",knnacc.std())

MLPnet = mlp.MLPNet()
MLPres = mlp.MLP_class(MLPnet,x[3],y)
print("MLP: acc: ",MLPres.mean(),"  std: ",MLPres.std())


CNNnet = ecn.ConvNet()
CNNres = ecn.FW_classby_CNN(CNNnet,x[3],y)
print("CNN: acc: ",CNNres.mean(),"  std: ",CNNres.std())

