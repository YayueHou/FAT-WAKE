
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import preprocess as pre
import EEGFileList as eeg
import seaborn as sns


# Use the following variables to control which to plot
PLOT_4DEVICE_SP_DIS=0
PLOT_4DEVICE_RWE_DIS=0
PLOT_4DEVICE_EN_DIS=1
PLOT_FWTGAM_SP_DIS=0
PLOT_FWTGAM_RWE_DIS=0
PLOT_FWTGAM_EN_DIS=0
PLOT_MUTGAM_SP_DIS=0
PLOT_MUTGAM_RWE_DIS=0
PLOT_MUTGAM_EN_DIS=0


# define color in thesis 
myblue="#4B33FF"
myred="#F24400"
myyellow="#C89C0E"
myorange="#994E0D"
mygreen="#03AC0F"


KSS=[]
delta, theta, alpha, beta, gamma, fi, KSS = [], [], [], [], [], [], []
SE,RE2,RE3,TsE,GenTsE= [],[],[],[],[]
A5,D5,D4,D3,D2,D1,RWE=[],[],[],[],[],[],[]
Device=[]
fat='Fatigue'
wak='Wake'

if(PLOT_MUTGAM_SP_DIS or PLOT_MUTGAM_RWE_DIS or PLOT_MUTGAM_EN_DIS):
   rest_start = 8
   rest_end = 32
   listen_start = 48
   listen_end = 72
   sample_rate = 512

   #TGAM FONRT
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FRONT_PATH,rest_start,rest_end,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Forehead FP1')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FRONT_PATH,listen_start,listen_end,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Forehead FP1')

   #TGAM EAR
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.EAR_PATH,rest_start,rest_end,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L5')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.EAR_PATH,listen_start,listen_end,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L5')

elif(PLOT_4DEVICE_SP_DIS or PLOT_4DEVICE_RWE_DIS or PLOT_4DEVICE_EN_DIS):

   #BrainLInk
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_BL,24,48,fat,delta,theta, alpha, beta, gamma, fi, KSS, SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='BrainLink')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_BL,78,102,fat,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='BrainLink')

   #UmindSleep
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_US,24,48,fat,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=256,device_name='UmindSleep')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_US,78,102,fat,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=256,device_name='UmindSleep')

   #EMOTIV
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_EM,24,48,fat,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=128,device_name='EMOTIV EPOC X')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_EM,78,102,fat,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=128,device_name='EMOTIV EPOC X')

   #UmindLIte
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_UL,24,48,fat,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=256,device_name='UmindLite')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.FATIGUE_UL,78,102,fat,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=256,device_name='UmindLite')

#######################################################################################################

   #BrainLink
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_BL,24,48,wak,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='BrainLink')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_BL,78,102,wak,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='BrainLink')

   #UmindSleep
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_US,24,48,wak,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=256,device_name='UmindSleep')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_US,78,102,wak,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=256,device_name='UmindSleep')

   #EMOTIV
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_EM,24,48,wak,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=128,device_name='EMOTIV EPOC X')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_EM,78,102,wak,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=128,device_name='EMOTIV EPOC X')

   #UmindLite
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_UL,24,48,wak,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=256,device_name='UmindLite')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.WAKE_UL,78,102,wak,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=256,device_name='UmindLite')

elif(PLOT_FWTGAM_SP_DIS or PLOT_FWTGAM_RWE_DIS or PLOT_FWTGAM_EN_DIS):
   #TGAM FONRT
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_F_FAT,24,48,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Forehead FP1')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_F_FAT,78,102,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Forehead FP1')

   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_F_WAK,24,48,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Forehead FP1')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_F_WAK,78,102,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Forehead FP1')

   ########################################################################################

   #EAR
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_E_FAT,24,48,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L3')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_E_FAT,78,102,0,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L3')

   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_E_WAK,24,48,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L3')
   delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,Device=pre.GetFeature(eeg.TGAM_E_WAK,78,102,1,delta,theta, alpha, beta, gamma, fi, KSS,SE,RE2,RE3,TsE,GenTsE,RWE,device=Device,sample_rate=512,device_name='Ear L3')

else:
   print("Error Selection")


# Try RWE as spectrum power
# delta=RWE[7]+RWE[6]+RWE[5]
# theta=RWE[4] 
# alpha=RWE[3]  
# beta=RWE[2]  
# gamma=RWE[0]+RWE[1] 


delta = numpy.array(delta)  
theta = numpy.array(theta)    
alpha = numpy.array(alpha)    
beta = numpy.array(beta)    
gamma = numpy.array(gamma)    
fi = numpy.array(fi)    

RWE=numpy.transpose(numpy.array(RWE))

Sp = [delta, theta, alpha, theta/beta, theta/alpha, theta/fi, theta/alpha+beta+gamma, delta/alpha+beta+gamma, delta/alpha, delta/fi, delta/beta, delta/theta, theta/alpha+beta+theta, alpha/theta+alpha+beta, beta/theta+alpha+beta]

Entropy=[SE,RE2,TsE,GenTsE]
Sp=numpy.array(Sp)

# define the general plot function of thesis
def plotdis(data,hue_data,x_data,legend_data,xxlim=None,yylim=None,col_name=None,bin_num=None ):
   sns.set_theme(style="white",font={'serif':'Times New Roman'},font_scale=1.8)
   if(bin_num==None):
      fig1=sns.displot(data,palette=[myred,myblue],x=x_data,hue=hue_data,kind='hist',kde=True,stat="density", common_norm=True,legend=False,col=col_name)
   else:
      fig1=sns.displot(data,palette=[myred,myblue],x=x_data,hue=hue_data,kind='hist',kde=True,stat="density", common_norm=True,legend=False,col=col_name,bins=bin_num)
   fig = plt.gca()
   fig.set_xlim(0,xxlim)
   fig.set_ylim(0,yylim)
   fig1.set_titles("{col_name}")
   plt.legend(legend_data,prop={'family' : 'Times New Roman', 'size': 24})



#################################### plot 4 device sp distribution #####################################
if(PLOT_4DEVICE_SP_DIS):
   Sp_D = []
   Sp_df = []
   xxlim=[1300,230,110,53,14,22,66,380,560,130,760,380,320,180,180]

   for i in range(0,15):
      Sp_D.append({ "State":KSS , ('Sp'+str(i+1) +' Value'):Sp[i] , 'Device':Device})
      Sp_df.append(pd.DataFrame(Sp_D[i]))
      plotdis(Sp_df[i],'State',('Sp'+str(i+1) +' Value'),['Fatigue','Wake'],xxlim=xxlim[i],col_name='Device')
   plt.show()
################################### finish plot 4 device sp distribution ##################################

############################## plot 4 device RWE Distribution #######################
if(PLOT_4DEVICE_RWE_DIS):
   Pi_D = []
   Pi_df = []
   for i in range(5):
      Pi_D.append({ "State":KSS , ('Level '+str(i+1)):RWE[i],'Device':Device})
      Pi_df.append(pd.DataFrame(Pi_D[i]))

   print(Pi_df)
   plotdis(Pi_df[0],'State',('Level 1'),['Fatigue','Wake'],col_name='Device')
   plotdis(Pi_df[1],'State',('Level 2'),['Fatigue','Wake'],col_name='Device')
   plotdis(Pi_df[2],'State',('Level 3'),['Fatigue','Wake'],col_name='Device')
   plotdis(Pi_df[3],'State',('Level 4'),['Fatigue','Wake'],col_name='Device')
   plotdis(Pi_df[4],'State',('Level 5'),['Fatigue','Wake'],col_name='Device')
   plt.show()
######################## finish plot 4 device RWE Distribution ######################

################################## plot 4 device Entorpy Distribution ####################################
if(PLOT_4DEVICE_EN_DIS):
   WEp = { "State":KSS , "WE Value":SE ,'Device':Device}
   REp = { "State":KSS , "RE Value":RE2 ,'Device':Device}
   TsEp = { "State":KSS , "TsE Value":TsE,'Device':Device }
   GenTsEp = { "State":KSS , "GenTsE Absolute Value":[abs(ele) for ele in GenTsE] ,'Device':Device}

   WEdf=pd.DataFrame(WEp)
   REdf=pd.DataFrame(REp)
   TsEdf=pd.DataFrame(TsEp)
   GenTsEdf=pd.DataFrame(GenTsEp)

   plotdis(WEdf,'State','WE Value',['Fatigue','Wake'],col_name='Device')
   plotdis(REdf,'State','RE Value',['Fatigue','Wake'],col_name='Device')
   plotdis(TsEdf,'State','TsE Value',['Fatigue','Wake'],col_name='Device')
   plotdis(GenTsEdf,'State','GenTsE Absolute Value',['Fatigue','Wake'],col_name='Device')
   plt.show()
################################# finish plot 4 device Entorpy Distribution ####################################


###################################### plot ear sp distribution #####################################
if(PLOT_FWTGAM_SP_DIS):
   Sp_D = []
   Sp_df = []
   xxlim=[4800,390,190,110,16,21,76,820,720,520,3100,270,470,190,190]
   for i in range(0,15):
      Sp_D.append({ "State":KSS , ('Sp'+str(i+1) +' Value'):Sp[i] , 'Electrode':Device})
      Sp_df.append(pd.DataFrame(Sp_D[i]))
      plotdis(Sp_df[i],'State',('Sp'+str(i+1) +' Value'),['Fatigue','Wake'],xxlim[i],col_name='Electrode')
   plt.show()
################################## finish ear plot sp distribution ##################################

#################################### plot ear RWE Distribution #####################################
if(PLOT_FWTGAM_RWE_DIS):
   Pi_D = []
   Pi_df = []
   for i in range(5):
      Pi_D.append({ "State":KSS , ('Level '+str(i+1)):RWE[i],'Electrode':Device})
      Pi_df.append(pd.DataFrame(Pi_D[i]))

   plotdis(Pi_df[0],'State',('Level 1'),['Fatigue','Wake'],col_name='Electrode')
   plotdis(Pi_df[1],'State',('Level 2'),['Fatigue','Wake'],col_name='Electrode')
   plotdis(Pi_df[2],'State',('Level 3'),['Fatigue','Wake'],col_name='Electrode')
   plotdis(Pi_df[3],'State',('Level 4'),['Fatigue','Wake'],col_name='Electrode')
   plotdis(Pi_df[4],'State',('Level 5'),['Fatigue','Wake'],col_name='Electrode')
   plt.show()
################################## finish plot ear RWE Distribution #################3################

################################### plot ear Entorpy Distribution #######################################
if(PLOT_FWTGAM_EN_DIS):
   WEp = { "State":KSS , "WE Value":SE ,'Electrode':Device}
   REp = { "State":KSS , "RE Value":RE2 ,'Electrode':Device}
   TsEp = { "State":KSS , "TsE Value":TsE,'Electrode':Device }
   GenTsEp = { "State":KSS , "GenTsE Absolute Value":[abs(ele) for ele in GenTsE] ,'Electrode':Device}

   WEdf=pd.DataFrame(WEp)
   REdf=pd.DataFrame(REp)
   TsEdf=pd.DataFrame(TsEp)
   GenTsEdf=pd.DataFrame(GenTsEp)
   plotdis(WEdf,'State','WE Value',['Fatigue','Wake'],col_name='Electrode')
   plotdis(REdf,'State','RE Value',['Fatigue','Wake'],col_name='Electrode')
   plotdis(TsEdf,'State','TsE Value',['Fatigue','Wake'],col_name='Electrode')
   plotdis(GenTsEdf,'State','GenTsE Absolute Value',['Fatigue','Wake'],col_name='Electrode')
   plt.show()
################################# finish plot ear Entorpy Distribution ##################################

###################################### plot music sp distribution #####################################
if(PLOT_MUTGAM_SP_DIS):
   Sp_D = []
   Sp_df = []
   xxlim=[4800,390,190,110,16,21,76,820,720,520,3100,270,470,190,190]
   for i in range(0,15):
      Sp_D.append({ "State":KSS , ('Sp'+str(i+1) +' Value'):Sp[i] , 'Electrode':Device})
      Sp_df.append(pd.DataFrame(Sp_D[i]))
      plotdis(Sp_df[i],'State',('Sp'+str(i+1) +' Value'),['Relax','Listen'],xxlim[i],col_name='Electrode')
   plt.show()
################################## finish music plot sp distribution ##################################

#################################### plot music RWE Distribution #####################################
if(PLOT_MUTGAM_RWE_DIS):
   Pi_D = []
   Pi_df = []
   for i in range(5):
      Pi_D.append({ "State":KSS , ('Level '+str(i+1)):RWE[i],'Electrode':Device})
      Pi_df.append(pd.DataFrame(Pi_D[i]))

   plotdis(Pi_df[0],'State',('Level 1'),['Relax','Listen'],col_name='Electrode')
   plotdis(Pi_df[1],'State',('Level 2'),['Relax','Listen'],col_name='Electrode')
   plotdis(Pi_df[2],'State',('Level 3'),['Relax','Listen'],col_name='Electrode')
   plotdis(Pi_df[3],'State',('Level 4'),['Relax','Listen'],col_name='Electrode')
   plotdis(Pi_df[4],'State',('Level 5'),['Relax','Listen'],col_name='Electrode')
   plt.show()
################################## finish plot music RWE Distribution #################3################

################################### plot music Entorpy Distribution #######################################
if(PLOT_MUTGAM_EN_DIS):
   WEp = { "State":KSS , "WE Value":SE ,'Electrode':Device}
   REp = { "State":KSS , "RE Value":RE2 ,'Electrode':Device}
   TsEp = { "State":KSS , "TsE Value":TsE,'Electrode':Device }
   GenTsEp = { "State":KSS , "GenTsE Absolute Value":[abs(ele) for ele in GenTsE] ,'Electrode':Device}

   WEdf=pd.DataFrame(WEp)
   REdf=pd.DataFrame(REp)
   TsEdf=pd.DataFrame(TsEp)
   GenTsEdf=pd.DataFrame(GenTsEp)
   plotdis(WEdf,'State','WE Value',['Relax','Listen'],col_name='Electrode')
   plotdis(REdf,'State','RE Value',['Relax','Listen'],col_name='Electrode')
   plotdis(TsEdf,'State','TsE Value',['Relax','Listen'],col_name='Electrode')
   plotdis(GenTsEdf,'State','GenTsE Absolute Value',['Relax','Listen'],col_name='Electrode')
   plt.show()
################################# finish plot music Entorpy Distribution ##################################
