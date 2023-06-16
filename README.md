# FAT-WAKE dataset
This dataset is used to study the commercial EEG wearable devices and their ability to detect drowsiness.
## Introduction
* Our data are acquisited by 5 devices: 
    - [Emotiv Epoc+](https://www.emotiv.com/epoc/)
    - [BrainLink](https://www.brainlink.org.au/)
    - [UmindLite](http://www.eegsmart.com/newsDetails.html?id=49&ran=0.9331091432832181)
    - [UmindSleep](http://www.eegsmart.com/en/UMindSleep.html)
    - [OpenBCI Cyton](https://shop.openbci.com/products/cyton-biosensing-board-8-channel)
* The experiment last about 15 minutes, with 19 participants.
* During the experiment Participants are asked to watching to a video. This video consist of 6 parts, which is shown as follows:
    - Relax (1min) -> Watch Video (4min) -> Relax (1min) -> Close Eyes (4min) -> Relax (1min) -> Watch Video (4min)
    - Each participant is required to take down their [KSS](https://link.springer.com/chapter/10.1007/978-1-4419-9893-4_47) value after they wathch the video.
    - When the participants are watching videos, their EEG signals are acquisited by the 5 devices. Each device has 5-7 participants EEG signal acquisited. 
* Our data is in `/FAT_WAKE_data`
* Our Processing code are in `data_process`
	- EEGFileList.py is the file name list
	- FW_Class_SVM_KNN.py is KNN and SVM defination
	- mlpeeg.py and eegcnn.py is mlp model and cnn model respectively
	- feature_selection.py contains the feature selection, F-Score calculation and classify after selection. Change the variables in the first several lines to choose selection options
	- FW_Classify.py contains all FAT-WAK experiment data classify. Change the variables in the first few lines to config the classify options.
	- TGAM_patern.py contains TGAM Music-Relax classify. Change the variables in the first few lines to config options.
* Our annotations are in `annotation`
* the methods to connect to devices are in `DeviceConnect`
* This dataset is also used to teach students in Tongji University, so you may find some tutorial comments.
## Usage
* Notice: the data are stored using lfs, so when clone please use
```
git lfs clone https://github.com/YayueHou/FAT-WAKE.git
```
* We could not promise that data download directly by `Download ZIP` is complete  
