# ANOVA feature selection for numeric input and categorical output

import numpy
import wavelet_entropy as waen
from scipy import signal 
import pandas as pd
import matplotlib.pyplot as plt
import preprocess as pre
import thesis_plot as tpl
import seaborn as sns
import EEGFileList as eeg
import FW_Class_SVM_KNN as fwcls
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

myblue="#003A6F"
#myblue="dark blue"
myred="#8B220D"
#myred="dark red"
myyellow="#C89C0E"
myorange="#994E0D"
mygreen="#336633"


# Use the following global variable to control
FW_TGAM_FRONT=0 # Print feature selection result of TGAM fronthead data
FW_TGAM_EAR=0   # Print feature selection result of TGAM earthead data
FW_TGAM_ALL=1   # Print feature selection result of all the TGAM data
FW_CLOSE=0      # Print feature selection result of all close eyes data
FW_OPEN=0       # Print feature selection result of all open eyes data
FW_ALL=0        # Print feature selection result of all data
FW_CLASS=1      # Print classification result of SVM and KNN after feature selection
FW_PLOT=1       # Plot feature score comparation
FEATURE_NUM=24  # features numbers to select
#SELECT_FUNCTION=mutual_info_classif
SELECT_FUNCTION=f_classif
#SCORE_NAME='F Score'
SCORE_NAME='Mutual Info'



KSS=[]

delta, theta, alpha, beta, gamma, fi, KSS = [], [], [], [], [], [], []
SE,RE2,RE3,TsE,GenTsE= [],[],[],[],[]
A5,D5,D4,D3,D2,D1,RWE=[],[],[],[],[],[],[]
Device=[]


def get_selected_frame(initial_data,KSS_annotation,feature_name,select_func,score_name,Hue_data,Hue_txt):
   fs = SelectKBest(score_func=select_func, k=FEATURE_NUM)
   fs=fs.fit(initial_data, KSS_annotation)
   feature_scores=pd.DataFrame(pre.normalize(fs.scores_))
   #feature_p=pd.DataFrame(Fscore.pvalues_)
   Hue_data=pd.DataFrame(Hue_data)
   scores_frame=pd.concat([feature_name,feature_scores,Hue_data],axis=1)
   scores_frame.columns = ['Feature',score_name, Hue_txt]
   ranked_score=scores_frame.nlargest(FEATURE_NUM,score_name)
   return fs,ranked_score,scores_frame


def class_selected_feature(feature_selection, initial_data,KSS_annotation, device_name):
   selected_data=feature_selection.transform(initial_data)
   KNN_acc,KNN_std=fwcls.FW_classby_KNN(selected_data, KSS_annotation)
   SVM_acc,SVM_std=fwcls.FW_classby_SVM(selected_data, KSS_annotation)
   print(device_name," SVM acc after selection: ", SVM_acc)
   print(device_name," SVM std after selection: ", SVM_std)
   print(device_name," KNN acc after selection: ", KNN_acc)
   print(device_name," KNN std after selection: ", KNN_std)
   print('---------------------------------------------')


#TGAM FONRT
if(FW_TGAM_FRONT or FW_TGAM_ALL):
   # FAT data
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_F_FAT,24,48,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=512,device_name='Forehead FP1',device=Device)
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_F_FAT,78,102,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=512,device_name='Forehead FP1',device=Device)
   # WAK data
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_F_WAK,24,48,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=512,device_name='Forehead FP1',device=Device)
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_F_WAK,78,102,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=512,device_name='Forehead FP1',device=Device)

#TGAM EAR
if(FW_TGAM_EAR or FW_TGAM_ALL):
   # EAR data
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_E_FAT,24,48,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L3')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_E_FAT,78,102,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L3')
   # EAR data
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_E_WAK,24,48,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L3')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_E_WAK,78,102,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L3')

# Open eye
if(FW_OPEN or FW_ALL):
   # BrainLink open eyes
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_BL,24,48,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=512,device=Device,device_name='Open_Eyes')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_BL,24,48,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=512,device=Device,device_name='Open_Eyes')
   # UmindSleep open eyes
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_US,24,48,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Open_Eyes')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_US,24,48,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Open_Eyes')
   # EMOTV open eyes
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_EM,24,48,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=128,device=Device,device_name='Open_Eyes')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_EM,24,48,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=128,device=Device,device_name='Open_Eyes')
   #UmindLite open eyes
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_UL,24,48,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Open_Eyes')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_UL,24,48,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Open_Eyes')

# Close eye
if(FW_CLOSE or FW_ALL):
   # BrainLink close eyes
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_BL,78,102,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=512,device=Device,device_name='Close_Eyes')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_BL,78,102,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=512,device=Device,device_name='Close_Eyes')
   # UmindSleep close eyes
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_US,78,102,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Close_Eyes')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_US,78,102,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Close_Eyes')
   # EMOTIV close eyes
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_EM,78,102,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=128,device=Device,device_name='Close_Eyes')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_EM,78,102,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=128,device=Device,device_name='Close_Eyes')
   # UmindLite close eyes
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_UL,78,102,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Close_Eyes')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_UL,78,102,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,sample_rate=256,device=Device,device_name='Close_Eyes')


# Use normal methods to calculate spectral features
delta = numpy.array(delta)  
theta = numpy.array(theta)    
alpha = numpy.array(alpha)    
beta = numpy.array(beta)    
gamma = numpy.array(gamma)    
fi = numpy.array(fi)    
RWE=numpy.transpose(numpy.array(RWE))


# Use wavelet coefficient to calculate spectral features 
# delta=RWE[7]+RWE[6]+RWE[5]
# theta=RWE[4]  # 4-8
# alpha=RWE[3]  # 8-16
# beta=RWE[2]   # 16-32
# gamma=RWE[0]+RWE[1] #64-128 32-64 


Sp = [delta, theta, alpha, theta/beta, theta/alpha, theta/fi, theta/alpha+beta+gamma, delta/alpha+beta+gamma, delta/alpha, delta/fi, delta/beta, delta/theta, theta/alpha+beta+theta, alpha/theta+alpha+beta, beta/theta+alpha+beta,SE,RE2,TsE,GenTsE]
Entropy=[SE,RE2,TsE,GenTsE]


# Stack all features together
X=numpy.transpose(numpy.vstack((Sp,RWE)))
y = numpy.transpose(numpy.array(KSS))

print(X.shape)
print(y.shape)

# Feature names in latex mode
# Sp_name1 =[r'$\delta$', r'$\theta$', r'$\alpha$', r'$\frac{\theta}{\beta}$', r'$\frac{\theta}{\alpha}$', r'$\frac{\theta}{\phi}$', r'$\frac{\theta}{\alpha}+\beta+\gamma$', r'$\frac{\delta}{\alpha}+\beta+\gamma$', r'$\frac{\delta}{\alpha}$', r'$\frac{\delta}{\phi}$', r'$\frac{\delta}{\beta}$', r'$\frac{\delta}{\theta}$', r'$\frac{\theta}{\alpha}+\beta+\theta$', r'$\frac{\alpha}{\theta}+\alpha+\beta$', r'$\frac{\beta}{\theta}+\alpha+\beta$','SE','RE2','TsE','GenTsE','Level1','Level2','Level3','Level4','Level5']

Sp_name=['Sp1','Sp2','Sp3','Sp4','Sp5','Sp6','Sp7','Sp8','Sp9','Sp10','Sp11','Sp12','Sp13','Sp14','Sp15','SE','RE2','TsE','GTsE','Lev1','Lev2','Lev3','Lev4','Lev5']
feature_name=pd.DataFrame(Sp_name)




# Select TGAM features
if(FW_TGAM_ALL):
   x_fro=X[0:int(X.shape[0]/2)]
   y_fro=y[0:int(y.shape[0]/2)]
   d_fro=Device[0:int(y.shape[0]/2)]
else:
   x_fro=X
   y_fro=y
   d_fro=Device

if(FW_TGAM_ALL):
   x_ear=X[int(X.shape[0]/2):]
   y_ear=y[int(X.shape[0]/2):]
   d_ear=Device[int(X.shape[0]/2):]
else:
   x_ear=X
   y_ear=y
   d_ear=Device


if(FW_TGAM_FRONT or FW_TGAM_ALL):
   fs_front,front_score,front_frame=get_selected_frame(x_fro,y_fro,feature_name,select_func=SELECT_FUNCTION,score_name=SCORE_NAME,Hue_data=d_fro,Hue_txt='Electrodes')
   print('--------FrontHead FP1 Selected Feature--------')
   print(front_score)
   print('----------------------------------------------')
   if(FW_CLASS):
      class_selected_feature(fs_front, x_fro, y_fro, 'TGAM FrontHead')


if(FW_TGAM_EAR or FW_TGAM_ALL):
   fs_ear,ear_score,ear_frame=get_selected_frame(x_ear,y_ear,feature_name,select_func=SELECT_FUNCTION,score_name=SCORE_NAME,Hue_data=d_ear,Hue_txt='Electrodes')
   print('--------AroundEar L3 Selected Feature---------')
   print(ear_score)
   print('----------------------------------------------')
   if(FW_CLASS):
      class_selected_feature(fs_ear, x_ear, y_ear, 'TGAM AroundEar')   


if(FW_TGAM_ALL):
   all_hue=[]
   for i in range(0,24):
      all_hue.append('Mix')
   tgam_all,tgam_score,tgam_frame=get_selected_frame(X,y,feature_name,select_func=SELECT_FUNCTION,score_name=SCORE_NAME,Hue_data=all_hue,Hue_txt='Electrodes')
   print('----------All TGAM Selected Feature----------')
   print(tgam_score)
   print('---------------------------------------------')
   if(FW_CLASS):
      class_selected_feature(tgam_all, X, y, 'TGAM All')


if(FW_PLOT and FW_TGAM_ALL):
   features=pd.concat([front_frame,ear_frame],axis=0)
   features.columns = ['Feature','Normalized '+SCORE_NAME,'Electrodes']
   sns.set_theme(style="white",font={'serif':'Times New Roman'},font_scale=1.3)
   #plt.figure(figsize=(10,6))
   plt.xticks(size=14)
   plt.yticks(size=14)
   #plt.xlabel('Feature',size=16)
   #plt.ylabel( 'F Score',size=16)
   sns.barplot(x="Feature", y="Normalized "+SCORE_NAME, hue="Electrodes", data=features,palette=[myblue,myred,mygreen],errorbar=None)
   plt.show()


if(FW_ALL):
   x_open=X[0:int(X.shape[0]/2)]
   y_open=y[0:int(y.shape[0]/2)]
   d_open=Device[0:int(y.shape[0]/2)]
else:
   x_open=X
   y_open=y
   d_open=Device

if(FW_ALL):
   x_close=X[int(X.shape[0]/2):]
   y_close=y[int(X.shape[0]/2):]
   d_close=Device[int(X.shape[0]/2):]
else:
   x_close=X
   y_close=y
   d_close=Device


if(FW_ALL or FW_OPEN):
   fs_open,open_score,open_frame=get_selected_frame(x_open, y_open, feature_name,select_func=SELECT_FUNCTION,score_name=SCORE_NAME,Hue_data=d_open,Hue_txt='Eyes State')
   print('----------Open Eyes Selected Feature----------')
   print(open_score)
   print('----------------------------------------------') 
   if(FW_CLASS):
      class_selected_feature(fs_open, x_open, y_open, 'Open Eyes')   
 

if(FW_ALL or FW_CLOSE):
   fs_close,close_score,close_frame=get_selected_frame(x_close, y_close, feature_name,select_func=SELECT_FUNCTION,score_name=SCORE_NAME,Hue_data=d_close,Hue_txt='Eyes State')
   print('---------Close Eyes Selected Feature----------')
   print(close_score)
   print('----------------------------------------------') 
   if(FW_CLASS):
      class_selected_feature(fs_close, x_close, y_close, 'Close Eyes')   


if(FW_ALL):
   eye=[]
   for i in range(0,24):
      eye.append('Mix')
   fs_all,all_score,all_frame=get_selected_frame(X, y, feature_name,select_func=SELECT_FUNCTION,score_name=SCORE_NAME,Hue_data=eye,Hue_txt='Eyes State')
   print('---------All States Selected Feature----------')
   print(all_score)
   print('----------------------------------------------') 
   if(FW_CLASS):
      class_selected_feature(fs_all, X, y, 'All States')   


if(FW_PLOT and FW_ALL):
   features=pd.concat([open_frame,close_frame,all_frame],axis=0)
   features.columns = ['Feature','Normalized '+SCORE_NAME,'Eyes State']
   sns.set_theme(style="white",font={'serif':'Times New Roman'},font_scale=1.2)
   plt.figure(figsize=(16,3.5))
   plt.xticks(size=14)
   plt.yticks(size=14)
   #plt.xlabel('Feature',size=16)
   #plt.ylabel( 'F Score',size=16)
   sns.barplot(x="Feature", y="Normalized "+SCORE_NAME, hue="Eyes State", data=features,palette=[myblue,myred,mygreen],errorbar=None)
   plt.show()


