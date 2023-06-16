import numpy
import preprocess as pre
import EEGFileList as eeg
import FW_Class_SVM_KNN as fwcl
import eegcnn as ecn
import mlpeeg as mlp

# Use the following variables to choose which data to classify
MU_TGAM_FRON=1
MU_TGAM_EAR=0
MU_TGAM_ALL=0


"""
Read txt datafiles: 
* cut the data into 5s/peice. The data is totally aroundd 14min long. 
* Consisit of 1min relax, 4min open eyes, 1min relax, 4min close eyes, 1min relax, 4min open eyes.
* use the signal between 2min-4min and 6.5min-8.5min

"""


KSS=[]

delta, theta, alpha, beta, gamma, fi, KSS = [], [], [], [], [], [], []
SE,RE2,RE3,TsE,GenTsE = [],[],[],[],[]
A5,D5,D4,D3,D2,D1,RWE = [],[],[],[],[],[],[]
Device=[]

rest_start = 8
rest_end = 32
listen_start = 48
listen_end = 72
sample_rate = 512

if(MU_TGAM_FRON or MU_TGAM_ALL):
#TGAM FONRT
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FRONT_PATH,rest_start,rest_end,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Forehead FP1')
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FRONT_PATH,listen_start,listen_end,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Forehead FP1')

if(MU_TGAM_EAR or MU_TGAM_ALL):
#TGAM EAR
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.EAR_PATH,rest_start,rest_end,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L5')
  delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.EAR_PATH,listen_start,listen_end,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L5')


delta = numpy.array(delta)  
theta = numpy.array(theta)    
alpha = numpy.array(alpha)    
beta = numpy.array(beta)    
gamma = numpy.array(gamma)    
fi = numpy.array(fi)    

RWE = numpy.transpose(numpy.array(RWE))
print(RWE[1].shape)


Sp = [delta, theta, alpha, theta/beta, theta/alpha, theta/fi, theta/alpha+beta+gamma, delta/alpha+beta+gamma, delta/alpha, delta/fi, delta/beta, delta/theta, theta/alpha+beta+theta, alpha/theta+alpha+beta, beta/theta+alpha+beta]

Entropy = [SE,RE2,TsE,GenTsE]

allf = [delta, theta, alpha, theta/beta, theta/alpha, theta/fi, theta/alpha+beta+gamma, delta/alpha+beta+gamma, delta/alpha, delta/fi, delta/beta, delta/theta, theta/alpha+beta+theta, alpha/theta+alpha+beta, beta/theta+alpha+beta,SE,RE2,TsE,GenTsE]

allf = numpy.array(allf)
y = numpy.transpose(numpy.array(KSS))

x = []

x.append(numpy.hstack((numpy.transpose(allf),numpy.transpose(RWE))))
x.append(numpy.transpose(numpy.array(Sp)))
x.append(numpy.transpose(RWE))
x.append(numpy.transpose(numpy.array(Entropy)))

for t in range(len(x)):
  print(x[t].shape)
  svmacc = fwcl.FW_classby_SVM(x[t],y)
  knnacc = fwcl.FW_classby_KNN(x[t],y)

  print("KNN: acc: ",knnacc.mean(),"  std: ",knnacc.std())
  print("SVM: acc: ",svmacc.mean(),"  std: ",svmacc.std())
  


MLPnet = mlp.MLPNet()
MLPres = mlp.MLP_class(MLPnet,x[0],y)
print("MLP: acc: ",MLPres.mean(),"  std: ",MLPres.std())


CNNnet = ecn.ConvNet()
CNNres = ecn.FW_classby_CNN(CNNnet,x[0],y)
print("CNN: acc: ",CNNres.mean(),"  std: ",CNNres.std())