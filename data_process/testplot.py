import numpy as np
import pyqtgraph as pg
import sys
from PyQt5.QtWidgets import QWidget,QApplication,QFrame,QGridLayout,QLabel,QPushButton,QVBoxLayout
from PyQt5.QtCore import Qt,QTimer
import threading
import serial
import joblib
import random
 

myblue="#003A6F"
#myblue="dark blue"
myred="#8B220D"
#myred="dark red"
myyellow="#C89C0E"
myorange="#994E0D"
mygreen="#336633"


d_data=[]


class EEGThread(QWidget):

    def __init__(self, parent=None):
        super(EEGThread, self).__init__(parent)
        self.ser = serial.Serial('COM22', 57600)
        self.bps = 57600
        self.vaul = []
        self.is_started = threading.Event()
        self.initUI()
        self.generate_image()
        self.data_wave = np.zeros(512)
        self.data_detect = []
        self.count=0
        self.state_='状态：清醒'
        self.tode=0


    def initUI(self):
        self.setGeometry(500,500,1500,600)
        self.setWindowTitle("脑电波形图")
        self.gridLayout = QGridLayout(self)
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.WinPanel)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.frame.setLineWidth(2)
        self.frame.setStyleSheet("background-color:rgb(255,255,255);")
        
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText('用户状态：  ')
        self.label.setAlignment(Qt.AlignCenter)
        self.button = QPushButton(self)
        self.button.setText("开始检测")
        self.button.clicked.connect(self.btnClick)
        self.gridLayout.addWidget(self.frame,0,1,2,1)
        self.gridLayout.addWidget(self.label,0,0,1,1)
        self.gridLayout.addWidget(self.button,1,0,1,1)
        self.setLayout(self.gridLayout)
        
        
    def generate_image(self):
        verticalLayout = QVBoxLayout(self.frame)
        win = pg.GraphicsLayoutWidget(self.frame)
        verticalLayout.addWidget(win)
        p = win.addPlot(title="EEG")
        p.showGrid(x=True,y=True)
        p.setLabel(axis="left",text="EEG / uV")
        p.setLabel(axis="bottom",text="samples/(1/512 s)")
        win.setBackground('w')
        p.setXRange(0, 512, padding=0)
        p.setYRange(-500, 500, padding=0)
        p.addLegend()

        self.curve1 = p.plot(pen="r",name="EEG")    
        self.t = np.arange(512)    #时间向量 1*1024的矩阵


    def btnClick(self):
        if(self.tode==0):
            self.button.setText("停止检测")
            self.tode=1
        else :
            self.button.setText("开始检测")
            self.tode=0
        timer = QTimer(self)
        timer.timeout.connect(self.plotData)
        timer.start(1)

    def plotData(self):
        global d_data,tode
        b = self.ser.readline()
        c=int(b.decode())
        self.data_wave[:-1] = self.data_wave[1:]
        self.data_wave[-1]=c-20
        self.curve1.setData(self.t , self.data_wave )
        print(c)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    eeg = EEGThread()
    eeg.show() 
    sys.exit(app.exec_())
